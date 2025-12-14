import tempfile
import uuid
import os
import json
import threading
from typing import Dict, Any, Optional
from fastapi.responses import FileResponse
from pydantic import FilePath
import redis
from logger import logger, TaskLogger
from process_launcher import run_engine_process
from config import Config
from file_utils import create_zip_from_folder, cleanup_tmp_files


class TaskManager:
    def __init__(self, redis_url: str = None, task_ttl: int = None):
        try:
            self.redis_url = redis_url or Config.get_redis_url()
            self.task_ttl = task_ttl or Config.TASK_TTL
            self.redis_client = redis.from_url(
                self.redis_url,
                decode_responses=True,
                socket_timeout=5,
                socket_connect_timeout=5,
                retry_on_timeout=True
            )
            self.redis_client.ping()
            self.task_prefix = "task:"
            self.pkg_index_prefix = "pkg_index:"  # 用于包名到task_id的映射
            logger.info(f"TaskManager initialized with Redis at {self.redis_url}")
        except redis.ConnectionError as e:
            logger.error(f"Failed to connect to Redis: {str(e)}")
            logger.error("Please ensure Redis is running: docker run -d --name redis-server -p 6379:6379 redis:latest")
            raise
        except Exception as e:
            logger.error(f"Error initializing TaskManager: {str(e)}")
            raise
        
    def get_task_collected_data(self, task_id):
        collect_data_path = FilePath(Config.COLLECTED_BASE_DIR) / task_id
        if not collect_data_path.exists():
            logger.error(f"Task collected data not found for task ID: {task_id}")
        
        if not collect_data_path.is_dir():
            logger.error(f"Task collected data is not a directory for task ID: {task_id}")
        
        if not any(collect_data_path.iterdir()):
            logger.error(f"Task collected data is empty for task ID: {task_id}")

        tmp_dir = tempfile.mkdtemp()
        zip_filename = f"task_{task_id}.zip"
        zip_path = os.path.join(tmp_dir, zip_filename)

        try:
            create_zip_from_folder(str(collect_data_path), zip_path)
            return FileResponse(
                path=zip_path,
                filename=zip_filename,
                media_type="application/zip",
                background=cleanup_tmp_files(zip_path, tmp_dir)
            )
        except Exception as e:
            logger.error(f"Error creating zip file for task {task_id}: {str(e)}")

    def find_task_by_package(self, pkg: str) -> Optional[str]:
        """
        通过包名查找对应的 task_id
        
        Args:
            pkg: 应用包名
            
        Returns:
            task_id 或 None（如果不存在）
        """
        try:
            index_key = f"{self.pkg_index_prefix}{pkg}"
            task_id = self.redis_client.get(index_key)
            
            if task_id:
                # 验证任务是否仍然存在
                task_data = self._get_task(task_id)
                if task_data:
                    logger.debug(f"Found task {task_id} for package {pkg}")
                    return task_id
                else:
                    # 任务已过期，删除索引
                    self.redis_client.delete(index_key)
                    logger.warning(f"Task {task_id} expired for package {pkg}, cleaned up index")
            
            return None
            
        except Exception as e:
            logger.error(f"Error finding task by package {pkg}: {str(e)}")
            return None

    def _save_pkg_index(self, pkg: str, task_id: str):
        """
        保存包名到 task_id 的映射索引
        
        Args:
            pkg: 应用包名
            task_id: 任务ID
        """
        try:
            index_key = f"{self.pkg_index_prefix}{pkg}"
            # 使用与任务相同的 TTL
            self.redis_client.setex(index_key, self.task_ttl, task_id)
            logger.debug(f"Saved package index: {pkg} -> {task_id}")
            return True
        except Exception as e:
            logger.error(f"Error saving package index for {pkg}: {str(e)}")
            return False

    def submit_task(self, pkg, app, timestamp: str = None):
        """提交任务：生成 task_id，初始化任务状态并启动后台线程"""
        try:
            task_id = str(uuid.uuid4())
            task_data = {
                "task_id": task_id,
                "pkg": pkg,
                "app": app,
                "status": "queued",
                "progress": 0.0,
                "message": "Waiting...",
                "log_file": None
            }
            
            # 如果提供了时间戳，也保存
            if timestamp:
                task_data["timestamp"] = timestamp

            self._save_task(task_id, task_data)
            # 保存包名索引
            self._save_pkg_index(pkg, task_id)
            
            # 使用 TaskLogger 记录任务提交
            TaskLogger.task_submitted(task_id, pkg, app)

            t = threading.Thread(
                target=self._run_task_wrapper,
                args=(task_id, pkg, app),
                daemon=True,
            )
            t.start()
            logger.info(f"Task {task_id} submitted and saved to Redis")
            return task_id

        except Exception as e:
            logger.error(f"Error in submit_task: {str(e)}")
            TaskLogger.task_failed("unknown", str(e))
            raise

    def get_status(self, task_id):
        """查询任务状态"""
        try:
            task_data = self._get_task(task_id)

            if task_data is None:
                logger.warning(f"Task {task_id} not found in Redis")
                return {
                    "status": "not_found",
                    "progress": 0,
                    "message": "Unknown task"
                }
            
            TaskLogger.status_queried(task_id)
            return {
                "task_id": task_data.get("task_id"),
                "pkg": task_data.get("pkg"),
                "app": task_data.get("app"),
                "status": task_data.get("status"),
                "progress": task_data.get("progress", 0),
                "message": task_data.get("message", ""),
                "log_file": task_data.get("log_file")
            }
        
        except Exception as e:
            logger.error(f"Error getting status for task {task_id}: {str(e)}")
            return {
                "status": "error",
                "progress": 0,
                "message": f"Error retrieving task status: {str(e)}"
            }
        
    def _run_task_wrapper(self, task_id, pkg, app):
        try:
            task_proxy = RedisTaskDict(self, task_id)
            run_engine_process(task_id, pkg, app, task_proxy)

        except Exception as e:
            logger.error(f"Error in task wrapper for {task_id}: {str(e)}")
            self.update_task_status(
                task_id,
                status="failed",
                progress=0,
                message=f"Task execution error: {str(e)}"
            )
    
    def update_task_status(self, task_id, **kwargs):
        try:
            task_data = self._get_task(task_id)

            if task_data is None:
                logger.warning(f"Cannot update non-existent task {task_id}")
                return False
            
            task_data.update(kwargs)
            self._save_task(task_id, task_data)
            logger.debug(f"Task {task_id} updated in Redis: {kwargs}")
            return True
        
        except Exception as e:
            logger.error(f"Error updating task {task_id}: {str(e)}")
            return False
    
    def _save_task(self, task_id, task_data):
        try:
            key = f"{self.task_prefix}{task_id}"
            value = json.dumps(task_data, ensure_ascii=False)
            self.redis_client.setex(key, self.task_ttl, value)
            return True
        except Exception as e:
            logger.error(f"Error saving task {task_id} to Redis: {str(e)}")
            return False
    
    def _get_task(self, task_id):
        try:
            key = f"{self.task_prefix}{task_id}"
            value = self.redis_client.get(key)

            if value is None:
                return None
            return json.loads(value)
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding task {task_id} data: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error getting task {task_id} from Redis: {str(e)}")
            return None
        
    def health_check(self):
        try:
            self.redis_client.ping()
            return True
        except Exception as e:
            logger.error(f"Redis health check failed: {str(e)}")
            return False
    
    def delete_task(self, task_id: str) -> bool:
        try:
            # 获取任务数据以便删除包名索引
            task_data = self._get_task(task_id)
            
            # 删除任务数据
            key = f"{self.task_prefix}{task_id}"
            self.redis_client.delete(key)
            
            # 删除包名索引
            if task_data and "pkg" in task_data:
                index_key = f"{self.pkg_index_prefix}{task_data['pkg']}"
                self.redis_client.delete(index_key)
            
            logger.info(f"Task {task_id} deleted from Redis")
            return True
        except Exception as e:
            logger.error(f"Error deleting task {task_id}: {str(e)}")
            return False
    
    def list_all_tasks(self) -> list:
        try:
            pattern = f"{self.task_prefix}*"
            keys = self.redis_client.keys(pattern)
            task_ids = [key.replace(self.task_prefix, "") for key in keys]
            return task_ids
        except Exception as e:
            logger.error(f"Error listing tasks: {str(e)}")
            return []


class RedisTaskDict:
    def __init__(self, manager: TaskManager, task_id: str):
        self.manager = manager
        self.task_id = task_id
    
    def __setitem__(self, key: str, value: Dict[str, Any]):
        if key == self.task_id:
            self.manager.update_task_status(self.task_id, **value)
    
    def __getitem__(self, key: str) -> Dict[str, Any]:
        if key == self.task_id:
            task_data = self.manager._get_task(self.task_id)
            return task_data if task_data else {}
        return {}
    
    def get(self, key: str, default=None) -> Dict[str, Any]:
        try:
            return self[key]
        except:
            return default if default is not None else {}
