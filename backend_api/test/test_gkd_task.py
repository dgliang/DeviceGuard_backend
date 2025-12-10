#!/usr/bin/env python3
"""
GKD 任务测试脚本
用于单独测试 GKD 部分，跳过 Poker 任务
"""

import sys
from pathlib import Path

# 添加项目路径到 sys.path
CURRENT_PATH = Path(__file__).parent  # test/
PROJECT_ROOT = CURRENT_PATH.parent    # 项目根目录
sys.path.insert(0, str(PROJECT_ROOT))

from process_launcher import run_gkd_task
from logger import logger


def main():
    # 配置测试参数
    task_id = "3d6b2360-ad00-43a5-a13a-a362f2932b7a"
    pkg = "com.xunmeng.pinduoduo"
    app = "拼多多"
    
    # 模拟已完成 Poker 任务的状态
    tasks_dict = {
        task_id: {
            "status": "completed",
            "message": "Poker already completed",
            "progress": 1.0,
            "log_file": f"logs/task_{task_id}.log"
        }
    }
    
    logger.info("=" * 60)
    logger.info("Starting GKD test")
    logger.info(f"Task ID: {task_id}")
    logger.info(f"Package: {pkg}")
    logger.info(f"App: {app}")
    logger.info("=" * 60)
    
    try:
        # 运行 GKD 任务
        run_gkd_task(task_id, pkg, app, tasks_dict)
        
        logger.info("=" * 60)
        logger.info("GKD test completed")
        logger.info(f"Final status: {tasks_dict[task_id]['status']}")
        logger.info(f"Final message: {tasks_dict[task_id]['message']}")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"GKD test failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()