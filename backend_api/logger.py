import logging
import sys
from pathlib import Path
from datetime import datetime
import json

# 创建logs目录
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# 创建任务日志目录
TASK_LOG_DIR = LOG_DIR / "tasks"
TASK_LOG_DIR.mkdir(exist_ok=True)

def setup_logger():
    """配置并返回logger实例"""
    
    # 创建logger
    logger = logging.getLogger("task_backend")
    logger.setLevel(logging.INFO)
    
    # 避免重复添加handler
    if logger.handlers:
        return logger
    
    # 日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    
    # 控制台handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # 文件handler - 按日期分割
    log_file = LOG_DIR / f"task_backend_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    
    # 错误日志文件handler
    error_file_handler = logging.FileHandler(LOG_DIR / "errors.log", encoding='utf-8')
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    
    # 添加handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(error_file_handler)
    
    return logger

# 创建全局logger实例
logger = setup_logger()

class TaskLogger:
    """任务专用的日志记录器"""
    
    @staticmethod
    def task_submitted(task_id: str, pkg: str, app: str):
        logger.info(f"Task submitted - ID: {task_id}, Package: {pkg}, App: {app}")
    
    @staticmethod
    def task_started(task_id: str):
        logger.info(f"Task started - ID: {task_id}")
    
    @staticmethod
    def task_completed(task_id: str, result: dict):
        logger.info(f"Task completed - ID: {task_id}, Result: {json.dumps(result, ensure_ascii=False)}")
    
    @staticmethod
    def task_failed(task_id: str, error: str):
        logger.error(f"Task failed - ID: {task_id}, Error: {error}")
    
    @staticmethod
    def task_progress(task_id: str, progress: int, message: str = ""):
        logger.info(f"Task progress - ID: {task_id}, Progress: {progress}%, Message: {message}")
    
    @staticmethod
    def status_queried(task_id: str):
        logger.debug(f"Status queried - ID: {task_id}")

    @staticmethod
    def get_task_log_path(task_id: str) -> Path:
        """获取任务日志文件路径"""
        return TASK_LOG_DIR / f"task_{task_id}.log"
    
    @staticmethod
    def create_task_log_file(task_id: str, pkg: str, app: str, cmd: str) -> Path:
        """创建任务日志文件并写入初始信息"""
        log_path = TaskLogger.get_task_log_path(task_id)
        
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(f"Task ID: {task_id}\n")
            f.write(f"Package: {pkg}\n")
            f.write(f"App: {app}\n")
            f.write(f"Command: {cmd}\n")
            f.write(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
        
        return log_path
    
    @staticmethod
    def append_task_log(task_id: str, content: str):
        """追加内容到任务日志文件"""
        log_path = TaskLogger.get_task_log_path(task_id)
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(content)
            if not content.endswith('\n'):
                f.write('\n')
    
    @staticmethod
    def finalize_task_log(task_id: str, returncode: int, status: str):
        """在任务日志文件末尾写入结束信息"""
        log_path = TaskLogger.get_task_log_path(task_id)
        
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write("\n" + "=" * 80 + "\n")
            f.write(f"Ended at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Status: {status}\n")
            f.write(f"Return code: {returncode}\n")
            f.write("=" * 80 + "\n")
    
    @staticmethod
    def engine_output(task_id: str, line: str):
        """记录引擎输出（同时写入主日志和任务日志）"""
        logger.debug(f"Task {task_id} - Engine: {line}")
        TaskLogger.append_task_log(task_id, f"[ENGINE] {line}")
