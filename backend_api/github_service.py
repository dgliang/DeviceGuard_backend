from pathlib import Path
from typing import Optional
import requests
from git import Repo, GitCommandError
from config import Config
from logger import logger


class GitHubService:
    """封装 GKD_subscription 仓库的 Git/GitHub 操作"""

    def __init__(self, repo_path: Optional[str] = None):
        self.repo_path = Path(repo_path or Config.GKD_REPO_PATH).resolve()
        if not self.repo_path.exists():
            raise FileNotFoundError(f"仓库路径不存在: {self.repo_path}")

        if not Config.GITHUB_TOKEN:
            raise ValueError("未配置 GITHUB_TOKEN")

        self.repo = Repo(self.repo_path)
        if self.repo.bare:
            raise ValueError(f"路径 {self.repo_path} 不是有效的 Git 仓库")

    def _checkout_base(self, base_branch: str):
        """拉取并切换到基准分支"""
        self.repo.git.fetch("origin", base_branch)
        self.repo.git.checkout(base_branch)
        self.repo.git.pull("origin", base_branch)

    def create_branch(self, branch_name: str, base_branch: Optional[str] = None) -> dict:
        base_branch = base_branch or Config.GITHUB_MAIN_BRANCH
        logger.info(f"准备创建/切换分支: {branch_name}, 基于: {base_branch}")

        try:
            self._checkout_base(base_branch)
            existing = branch_name in self.repo.heads
            self.repo.git.checkout("-B", branch_name, base_branch)
        except GitCommandError as e:
            logger.error(f"创建分支失败: {e}")
            raise RuntimeError(f"创建分支失败: {e}") from e

        return {
            "branch": branch_name,
            "base_branch": base_branch,
            "created": not existing,
            "path": str(self.repo_path),
        }

    def push_branch(self, branch_name: str) -> dict:
        logger.info(f"推送分支到远程: {branch_name}")
        try:
            self.repo.git.checkout(branch_name)
            push_result = self.repo.git.push("--set-upstream", "origin", branch_name)
        except GitCommandError as e:
            logger.error(f"推送分支失败: {e}")
            raise RuntimeError(f"推送分支失败: {e}") from e
        return {
            "branch": branch_name,
            "result": push_result,
        }

    def create_pull_request(
        self,
        branch_name: str,
        base_branch: Optional[str] = None,
        title: Optional[str] = None,
        body: Optional[str] = None,
    ) -> dict:
        base_branch = base_branch or Config.GITHUB_MAIN_BRANCH
        owner = Config.GITHUB_OWNER
        repo_name = Config.GITHUB_REPO
        api_base = Config.GITHUB_API_BASE.rstrip("/")
        url = f"{api_base}/repos/{owner}/{repo_name}/pulls"

        payload = {
            "title": title or f"{branch_name} -> {base_branch}",
            "head": f"{owner}:{branch_name}",
            "base": base_branch,
        }
        if body:
            payload["body"] = body

        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {Config.GITHUB_TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=15)
        except requests.RequestException as e:
            logger.error(f"请求 GitHub 创建 PR 失败: {e}")
            raise RuntimeError(f"请求 GitHub 创建 PR 失败: {e}") from e
        if resp.status_code not in (200, 201):
            logger.error(f"创建 PR 失败: {resp.status_code} - {resp.text}")
            raise RuntimeError(f"创建 PR 失败: {resp.status_code} - {resp.text}")

        data = resp.json()
        return {
            "html_url": data.get("html_url"),
            "number": data.get("number"),
            "state": data.get("state"),
            "title": data.get("title"),
        }

    def trigger_workflow(self, ref: Optional[str] = None, workflow: Optional[str] = None) -> dict:
        ref = ref or Config.GITHUB_MAIN_BRANCH
        workflow = workflow or Config.GITHUB_WORKFLOW_FILE
        owner = Config.GITHUB_OWNER
        repo_name = Config.GITHUB_REPO
        api_base = Config.GITHUB_API_BASE.rstrip("/")
        url = f"{api_base}/repos/{owner}/{repo_name}/actions/workflows/{workflow}/dispatches"

        payload = {"ref": ref}
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {Config.GITHUB_TOKEN}",
            "Content-Type": "application/json",
        }

        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=15)
        except requests.RequestException as e:
            logger.error(f"请求 GitHub 触发工作流失败: {e}")
            raise RuntimeError(f"请求 GitHub 触发工作流失败: {e}") from e
        if resp.status_code != 204:
            logger.error(f"触发工作流失败: {resp.status_code} - {resp.text}")
            raise RuntimeError(f"触发工作流失败: {resp.status_code} - {resp.text}")

        return {
            "workflow": workflow,
            "ref": ref,
            "status": "triggered",
            "actions_url": f"https://github.com/{owner}/{repo_name}/actions",
        }
    
    def merge_pull_request(
        self,
        pr_number: int,
        merge_method: str = "merge",
        commit_title: Optional[str] = None,
        commit_message: Optional[str] = None,
    ) -> dict:
        owner = Config.GITHUB_OWNER
        repo_name = Config.GITHUB_REPO
        api_base = Config.GITHUB_API_BASE.rstrip("/")
        url = f"{api_base}/repos/{owner}/{repo_name}/pulls/{pr_number}/merge"

        payload = {
            "merge_method": merge_method,
        }
        if commit_title:
            payload["commit_title"] = commit_title
        if commit_message:
            payload["commit_message"] = commit_message

        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {Config.GITHUB_TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        try:
            resp = requests.put(url, json=payload, headers=headers, timeout=15)
        except requests.RequestException as e:
            logger.error(f"请求 GitHub 合并 PR 失败: {e}")
            raise RuntimeError(f"请求 GitHub 合并 PR 失败: {e}") from e
        
        if resp.status_code == 200:
            data = resp.json()
            logger.info(f"PR #{pr_number} 合并成功: {data.get('sha')}")
            return {
                "merged": True,
                "sha": data.get("sha"),
                "message": data.get("message"),
            }
        elif resp.status_code == 405:
            # PR 不可合并（例如有冲突、未通过检查等）
            logger.warning(f"PR #{pr_number} 无法合并: {resp.text}")
            return {
                "merged": False,
                "reason": "not_mergeable",
                "detail": resp.text,
            }
        else:
            logger.error(f"合并 PR 失败: {resp.status_code} - {resp.text}")
            raise RuntimeError(f"合并 PR 失败: {resp.status_code} - {resp.text}")
