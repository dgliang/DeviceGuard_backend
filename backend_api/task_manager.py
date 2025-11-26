import uuid
import threading
from logger import logger, TaskLogger
from process_launcher import run_engine_process


class TaskManager:
    def __init__(self):
        self.tasks = {}  # task_id -> {status, progress}
        logger.info("TaskManager initialized")

    def submit_task(self, pkg, app):
        """提交任务：生成 task_id，初始化任务状态并启动后台线程"""
        try:
            task_id = str(uuid.uuid4())
            self.tasks[task_id] = {
                "status": "queued",
                "progress": 0.0,
                "message": "Waiting..."
            }

            # 使用 TaskLogger 记录任务提交
            TaskLogger.task_submitted(task_id, pkg, app)

            t = threading.Thread(
                target=run_engine_process,
                args=(task_id, pkg, app, self.tasks),
                daemon=True,
            )
            t.start()

            return task_id

        except Exception as e:
            logger.error(f"Error in submit_task: {str(e)}")
            TaskLogger.task_failed("unknown", str(e))
            raise

    def get_status(self, task_id):
        """查询任务状态"""
        status = self.tasks.get(task_id, {
            "status": "not_found",
            "progress": 0,
            "message": "Unknown task"
        })

        # 记录状态查询操作（debug 级别）
        TaskLogger.status_queried(task_id)

        return status
