import datetime
from fastapi import FastAPI, HTTPException
from models.task_models import TaskRequest, TaskStatusResponse
from task_manager import TaskManager
from logger import logger, TaskLogger

app = FastAPI()
task_manager = TaskManager()

@app.post("/api/run", response_model=dict)
async def run_single_app(req: TaskRequest):
    """
    接受单个 app 的数据收集请求
    """
    try:
        logger.info(f"Received task request - Package: {req.pkg}, App: {req.app}")
        
        task_id = task_manager.submit_task(req.pkg, req.app)
        
        # 记录任务提交
        TaskLogger.task_submitted(task_id, req.pkg, req.app)
        
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
        
        # 记录状态查询
        TaskLogger.status_queried(task_id)
        
        logger.debug(f"Status query successful - Task: {task_id}, Status: {status.status}")
        return status
        
    except Exception as e:
        logger.error(f"Error querying task status - ID: {task_id}, Error: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Task not found: {task_id}")

@app.get("/health")
async def health_check():
    """健康检查端点"""
    logger.debug("Health check requested")
    return {"status": "healthy", "timestamp": datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat()}

# # 全局异常处理
# @app.exception_handler(Exception)
# async def global_exception_handler(request, exc):
#     logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
#     return JSONResponse(
#         status_code=500,
#         content={"detail": "Internal server error"}
#     )