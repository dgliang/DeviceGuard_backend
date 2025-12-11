import subprocess
import time
import sys
import os
from logger import TaskLogger, logger
from pathlib import Path
from config import Config


CURRENT_PATH = Path(__file__).parent.parent
POKER_PATH = CURRENT_PATH / "poker"
POKER_ENGINE_PATH = CURRENT_PATH / "poker" / "poker_engine.py"
GKD_PATH = CURRENT_PATH / "GKD_subscription"
GKD_ENGINE_PATH = CURRENT_PATH / "GKD_subscription" / "run_match_ele.py"
PYTHON_EXEC = "python3" if sys.platform != "win32" else "python"


def run_engine_process(task_id, pkg, app, tasks_dict):
    """主入口函数：依次运行 Poker 和 GKD 任务"""
    # 更新任务状态
    tasks_dict[task_id]["status"] = "running"
    tasks_dict[task_id]["message"] = "Engine started"
    tasks_dict[task_id]["progress"] = 0.0

    # 记录任务开始
    TaskLogger.task_started(task_id)

    try:
        # 执行 Poker 任务
        poker_success = run_poker_task(task_id, pkg, app, tasks_dict)
        
        # Poker 任务成功后，执行 GKD 任务
        gkd_success = False
        if poker_success and GKD_ENGINE_PATH and GKD_ENGINE_PATH.exists():
            logger.info(f"Task {task_id} - Poker task completed, starting GKD task")
            try:
                gkd_success = run_gkd_task(task_id, pkg, app, tasks_dict)
            except Exception as e:
                logger.error(f"Task {task_id} - GKD task failed: {str(e)}")
                TaskLogger.append_task_log(task_id, f"[GKD] Error: {str(e)}")
            
        if poker_success and gkd_success:
            logger.info(f"Task {task_id} - Poker and GKD completed, starting GitHub task")
            TaskLogger.append_task_log(task_id, f"[GitHub] Starting GitHub task...")

            try:
                github_result = run_github_task(Config.GKD_REPO_PATH, Config.GITHUB_MAIN_BRANCH, "test/api")
                if github_result["status"] == "completed":
                    logger.info(f"Task {task_id} - GitHub task completed successfully")
                    TaskLogger.append_task_log(task_id, f"[GitHub] Task completed successfully")
                    TaskLogger.append_task_log(task_id, f"[GitHub] PR: {github_result.get('pr', {}).get('url', 'N/A')}")
                    tasks_dict[task_id]["message"] = "All tasks completed (Poker + GKD + GitHub)"
                    tasks_dict[task_id]["github_result"] = github_result
                elif github_result["status"] == "skipped":
                    logger.info(f"Task {task_id} - GitHub task skipped: {github_result.get('reason', 'unknown')}")
                    TaskLogger.append_task_log(task_id, f"[GitHub] Skipped: {github_result.get('reason', 'unknown')}")
                    tasks_dict[task_id]["message"] = "Poker and GKD completed (GitHub skipped)"
                    
            except Exception as e:
                error_text = str(e)
                logger.error(f"Task {task_id} - GitHub task failed: {error_text}")
                TaskLogger.append_task_log(task_id, f"[GitHub] Error: {error_text}")
                # GitHub 失败不影响整体任务状态，因为 Poker 和 GKD 已成功
                tasks_dict[task_id]["message"] = f"Poker and GKD completed, but GitHub failed: {error_text}"
        else:
            logger.info(f"Task {task_id} - Skipping GitHub task (prerequisite tasks not successful)")

    except Exception as e:
        error_text = str(e)
        tasks_dict[task_id]["status"] = "failed"
        tasks_dict[task_id]["message"] = error_text
        TaskLogger.task_failed(task_id, error_text)


def run_poker_task(task_id, pkg, app, tasks_dict):
    """运行 Poker 引擎任务"""
    try:
        cmd = [
            PYTHON_EXEC,
            str(POKER_ENGINE_PATH),
            "--pkg",
            pkg,
            "--app",
            app,
            "--task_id",
            task_id
        ]

        cmd_str = ' '.join(cmd)
        logger.info(f"Task {task_id} - Executing Poker: {cmd_str}")
        
        # 创建任务日志文件
        log_path = TaskLogger.create_task_log_file(task_id, pkg, app, cmd_str)
        tasks_dict[task_id]["log_file"] = str(log_path)
        logger.info(f"Task {task_id} - Log file: {log_path}")

        # 启动进程，输出重定向到日志文件
        with open(log_path, 'a', encoding='utf-8') as log_file:
            proc = subprocess.Popen(
                cmd,
                cwd=str(POKER_PATH),
                stdout=log_file,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )

        stdout, stderr = proc.communicate()

        if proc.returncode == 0:
            tasks_dict[task_id]["status"] = "completed"
            tasks_dict[task_id]["message"] = "Poker task finished"
            tasks_dict[task_id]["progress"] = 1.0

            # 记录任务完成
            result = {
                "status": "completed",
                "returncode": proc.returncode,
                "message": tasks_dict[task_id]["message"],
            }
            TaskLogger.task_completed(task_id, result)
            return True
        else:
            tasks_dict[task_id]["status"] = "failed"
            error_msg = (stderr.strip() if stderr else None) or "Poker process failed"
            tasks_dict[task_id]["message"] = error_msg
            tasks_dict[task_id]["progress"] = tasks_dict[task_id].get("progress", 0.0)

            # 记录任务失败
            TaskLogger.task_failed(task_id, error_msg)
            return False

    except Exception as e:
        error_text = str(e)
        tasks_dict[task_id]["status"] = "failed"
        tasks_dict[task_id]["message"] = error_text
        TaskLogger.task_failed(task_id, error_text)
        return False


def run_gkd_task(task_id, pkg, app, tasks_dict):
    """运行 GKD 任务"""
    logger.info(f"Task {task_id} - Starting GKD task")
    TaskLogger.append_task_log(task_id, f"[GKD] Starting GKD task...")
    
    tasks_dict[task_id]["message"] = "Running GKD task..."
    TaskLogger.append_task_log(task_id, f"[GKD] Message: Running GKD task...")
    
    try:
        script_path = GKD_ENGINE_PATH
        if not script_path or not script_path.exists():
            error_msg = f"GKD script not found: {script_path}"
            logger.error(f"Task {task_id} - {error_msg}")
            TaskLogger.append_task_log(task_id, f"[GKD] Error: {error_msg}")
            tasks_dict[task_id]["status"] = "failed"
            tasks_dict[task_id]["message"] = error_msg
            TaskLogger.task_failed(task_id, error_msg)
            return False
        
        working_dir = str(GKD_PATH) if GKD_PATH else str(script_path.parent)
        
        cmd = [
            PYTHON_EXEC,
            str(script_path),
            task_id,
        ]
        
        cmd_str = ' '.join(cmd)
        logger.info(f"Task {task_id} - GKD task executing: {cmd_str}")
        TaskLogger.append_task_log(task_id, f"[GKD] Executing: {cmd_str}")
        
        log_path = tasks_dict[task_id].get("log_file")
        if not log_path:
            log_path = TaskLogger.create_task_log_file(task_id, pkg, app, cmd_str)
        
        with open(log_path, 'a', encoding='utf-8') as log_file:
            log_file.write(f"\n{'='*60}\n")
            log_file.write(f"[GKD] Starting at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            log_file.write(f"[GKD] Command: {cmd_str}\n")
            log_file.write(f"{'='*60}\n")
            
            cli_proc = subprocess.Popen(
                cmd,
                cwd=working_dir,
                stdout=log_file,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
        
        cli_stdout, cli_stderr = cli_proc.communicate()
        
        with open(log_path, 'a', encoding='utf-8') as log_file:
            log_file.write(f"\n{'='*60}\n")
            log_file.write(f"[GKD] Completed at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            log_file.write(f"[GKD] Return code: {cli_proc.returncode}\n")
            log_file.write(f"{'='*60}\n")
        
        if cli_proc.returncode == 0:
            logger.info(f"Task {task_id} - GKD task completed successfully")
            TaskLogger.append_task_log(task_id, f"[GKD] Completed successfully")
            tasks_dict[task_id]["message"] = "Poker and GKD completed"
            return True
        else:
            error_msg = (cli_stderr.strip() if cli_stderr else None) or f"GKD task failed with return code {cli_proc.returncode}"
            logger.warning(f"Task {task_id} - GKD task failed: {error_msg}")
            TaskLogger.append_task_log(task_id, f"[GKD] Failed: {error_msg}")
            tasks_dict[task_id]["message"] = f"Poker completed, but GKD failed: {error_msg}"
            return False
            
    except Exception as e:
        error_text = str(e)
        logger.error(f"Task {task_id} - GKD task exception: {error_text}")
        TaskLogger.append_task_log(task_id, f"[GKD] Exception: {error_text}")
        tasks_dict[task_id]["status"] = "failed"
        tasks_dict[task_id]["message"] = f"GKD task exception: {error_text}"
        TaskLogger.task_failed(task_id, error_text)
        return False


def run_github_task(repo_path, base_branch, remote_branch):
    """
    GitHub任务：检查仓库状态 -> 有改动则提交到远端分支 -> 创建 PR -> 触发主分支流水线
    """
    from github_service import GitHubService

    service = GitHubService(repo_path)
    repo = service.repo

    # 1) 无改动则直接返回
    if not repo.is_dirty(untracked_files=True):
        logger.info("GitHub task skipped: no changes in working tree")
        return {"status": "skipped", "reason": "no changes"}

    try:
        # 2) 切换/创建工作分支
        branch_info = service.create_branch(remote_branch, base_branch)

        # 3) 暂存并提交
        repo.git.add(all=True)
        staged_diff = repo.index.diff("HEAD")
        if not staged_diff:
            logger.info("GitHub task skipped: nothing to commit after add")
            return {"status": "skipped", "reason": "nothing to commit"}

        commit_msg = f"chore: sync updates for {remote_branch}"
        repo.index.commit(commit_msg)
        logger.info(f"Committed changes with message: {commit_msg}")

        # 4) 推送分支（若远端不存在会创建）
        push_info = service.push_branch(remote_branch)

        # 5) 创建 PR
        pr_title = f"{remote_branch} -> {base_branch}"
        pr_info = service.create_pull_request(
            branch_name=remote_branch,
            base_branch=base_branch,
            title=pr_title,
        )

        # 6) 触发主分支构建/发布流水线
        workflow_info = service.trigger_workflow(ref=base_branch)

        result = {
            "status": "completed",
            "branch": branch_info,
            "push": push_info,
            "pr": pr_info,
            "workflow": workflow_info,
        }
        logger.info(f"GitHub task completed: {result}")
        return result

    except Exception as e:
        logger.error(f"GitHub task failed: {e}")
        raise
