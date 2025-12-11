#! /usr/bin/env python3

import sys
from pathlib import Path

CURRENT_PATH = Path(__file__).parent  # test/
PROJECT_ROOT = CURRENT_PATH.parent    # 项目根目录
sys.path.insert(0, str(PROJECT_ROOT))

from github_service import GitHubService

def test_init():
    print("=== test_init ===")
    try:
        svc = GitHubService(repo_path=str(PROJECT_ROOT.parent / "GKD_subscription"))
        print("初始化成功")
        print("repo path:", svc.repo_path)
        print("current branch:", svc.repo.active_branch)
    except Exception as e:
        print("初始化失败:", e)

def test_create_branch():
    print("=== test_create_branch ===")
    branch_name = "test/console-branch"

    try:
        svc = GitHubService(repo_path=str(PROJECT_ROOT.parent / "GKD_subscription"))
        result = svc.create_branch(branch_name)
        print("创建/切换分支成功")
        print(result)
        print("当前分支:", svc.repo.active_branch)
    except Exception as e:
        print("创建分支失败:", e)

def test_push_branch():
    print("=== test_push_branch ===")
    branch_name = "test/console-branch"

    try:
        svc = GitHubService(repo_path=str(PROJECT_ROOT.parent / "GKD_subscription"))
        result = svc.push_branch(branch_name)
        print("推送成功")
        print(result)
    except Exception as e:
        print("推送失败:", e)

def test_create_pr():
    print("=== test_create_pr ===")
    branch_name = "test/console-branch"

    try:
        svc = GitHubService(repo_path=str(PROJECT_ROOT.parent / "GKD_subscription"))
        pr = svc.create_pull_request(
            branch_name=branch_name,
            title="test: console PR",
            body="这是一个控制台测试 PR"
        )
        print("PR 创建成功")
        print(pr)
    except Exception as e:
        print("创建 PR 失败:", e)

def test_trigger_workflow():
    print("=== test_trigger_workflow ===")

    try:
        svc = GitHubService(repo_path=str(PROJECT_ROOT.parent / "GKD_subscription"))
        result = svc.trigger_workflow(ref="test/console-branch")
        print("工作流触发成功")
        print(result)
    except Exception as e:
        print("触发工作流失败:", e)

if __name__ == "__main__":
    test_init()
    test_create_branch()
    test_push_branch()
    test_create_pr()
    test_trigger_workflow()
