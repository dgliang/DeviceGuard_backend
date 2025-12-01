import datetime
from fastapi import FastAPI, HTTPException
from models.task_models import TaskRequest, TaskStatusResponse
from task_manager import TaskManager
from logger import logger, TaskLogger
from config import Config

app = FastAPI()
try:
    task_manager = TaskManager(redis_url=Config.get_redis_url(), task_ttl=Config.TASK_TTL)
except Exception as e:
    logger.error(f"Failed to initialize TaskManager: {str(e)}")
    raise

@app.post("/api/run", response_model=dict)
async def run_single_app(req: TaskRequest):
    """
    接受单个 app 的数据收集请求
    """
    try:
        logger.info(f"Received task request - Package: {req.pkg}, App: {req.app}")
        
        task_id = task_manager.submit_task(req.pkg, req.app)
        
        logger.info(f"Task submitted successfully - ID: {task_id}")
        return {"task_id": task_id}
        
    except Exception as e:
        logger.error(f"Error submitting task - Package: {req.pkg}, App: {req.app}, Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Task submission failed: {str(e)}")

@app.get("/api/task/{task_id}/status", response_model=TaskStatusResponse)
async def get_status(task_id: str):
    """
    查询任务执行状态和进度
    """
    try:
        logger.debug(f"Querying status for task: {task_id}")
        
        status = task_manager.get_status(task_id)
        
        if status.get("status") == "not_found":
            raise HTTPException(status_code=404, detail=f"Task not found: {task_id}")
        
        logger.debug(f"Status query successful - Task: {task_id}, Status: {status.get('status')}")
        return status
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error querying task status - ID: {task_id}, Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving task status: {str(e)}")

@app.get("/health")
async def health_check():
    """健康检查端点"""
    logger.debug("Health check requested")
    redis_healthy = task_manager.health_check()
    return {
        "status": "healthy" if redis_healthy else "degraded",
        "redis": "connected" if redis_healthy else "disconnected",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat()
    }

# # 全局异常处理
# @app.exception_handler(Exception)
# async def global_exception_handler(request, exc):
#     logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
#     return JSONResponse(
#         status_code=500,
#         content={"detail": "Internal server error"}
#     )

@app.get("/api/tasks", response_model=dict)
async def list_tasks():
    """
    列出所有任务
    """
    try:
        task_ids = task_manager.list_all_tasks()
        return {
            "total": len(task_ids),
            "task_ids": task_ids
        }
    except Exception as e:
        logger.error(f"Error listing tasks: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error listing tasks: {str(e)}")
