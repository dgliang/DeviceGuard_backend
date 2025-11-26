import subprocess
import time
import sys
import os
from logger import TaskLogger, logger
from pathlib import Path

# ENGINE_PATH = "../poker/poker_engine.py"
CURRENT_PATH = Path(__file__).parent.parent
POKER_PATH = CURRENT_PATH / "poker"
ENGINE_PATH = CURRENT_PATH / "poker" / "poker_engine.py"
PYTHON_EXEC = "python3" if sys.platform != "win32" else "python"


def run_engine_process(task_id, pkg, app, tasks_dict):
    # 更新任务状态
    tasks_dict[task_id]["status"] = "running"
    tasks_dict[task_id]["message"] = "Engine started"
    tasks_dict[task_id]["progress"] = 0.0

    # 记录任务开始
    TaskLogger.task_started(task_id)

    try:
        cmd = [
            PYTHON_EXEC,
            str(ENGINE_PATH),
            "--pkg",
            pkg,
            "--app",
            app,
        ]

        cmd_str = ' '.join(cmd)
        logger.info(f"Task {task_id} - Executing: {cmd_str}")
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
                stderr=subprocess.STDOUT,  # 合并 stderr 到 stdout
                text=True,
                bufsize=1,  # 行缓冲，实时写入
            )

        # # 进度模拟（未来可接入真实进度）
        # total_steps = 10
        # for i in range(total_steps):
        #     # 子进程已退出则停止模拟进度
        #     if proc.poll() is not None:
        #         break

        #     time.sleep(3)
        #     progress = (i + 1) / total_steps
        #     tasks_dict[task_id]["progress"] = progress
        #     # 使用整数百分比记录日志
        #     TaskLogger.task_progress(
        #         task_id,
        #         int(progress * 100),
        #         message="Engine processing",
        #     )

        stdout, stderr = proc.communicate()

        if proc.returncode == 0:
            tasks_dict[task_id]["status"] = "completed"
            tasks_dict[task_id]["message"] = "Finished"
            tasks_dict[task_id]["progress"] = 1.0

            # 记录任务完成，带简单结果信息
            result = {
                "status": "completed",
                "returncode": proc.returncode,
                "message": tasks_dict[task_id]["message"],
            }
            TaskLogger.task_completed(task_id, result)
        else:
            tasks_dict[task_id]["status"] = "failed"
            error_msg = stderr.strip() or "Engine process failed"
            tasks_dict[task_id]["message"] = error_msg
            tasks_dict[task_id]["progress"] = tasks_dict[task_id].get(
                "progress", 0.0
            )

            # 记录任务失败，包含错误信息
            TaskLogger.task_failed(task_id, error_msg)

    except Exception as e:
        error_text = str(e)
        tasks_dict[task_id]["status"] = "failed"
        tasks_dict[task_id]["message"] = error_text

        # 记录异常失败
        TaskLogger.task_failed(task_id, error_text)
