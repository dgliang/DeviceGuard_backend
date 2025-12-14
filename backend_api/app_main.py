import datetime
from fastapi import FastAPI, HTTPException
from models.task_models import TaskRequest, TaskStatusResponse, RunTaskRequest, MultipleTaskRequest, MultipleRunTaskRequest
from task_manager import TaskManager
from logger import logger
from config import Config
from adb_service import ADBAppManager
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    task_manager = TaskManager(redis_url=Config.get_redis_url(), task_ttl=Config.TASK_TTL)
except Exception as e:
    logger.error(f"Failed to initialize TaskManager: {str(e)}")
    raise

##################################################
# 前端要求的 API 接口
##################################################

@app.get("/api/apps")
async def get_third_party_apps():
    """
    通过 ADB 获取手机上所有第三方下载的的包名和应用名
    """
    try:
        logger.info("Getting all third party apps from device via ADB")
        apps = ADBAppManager.get_all_third_party_apps(verbose=True)
        return {
            "total": len(apps),
            "apps": apps
        }
    except Exception as e:
        logger.error(f"Error getting all third party apps: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting all third party apps: {str(e)}")

@app.get("/api/connect")
async def connect_device():
    """
    通过 ADB 连接设备
    """
    try:
        logger.info("Connecting to device via ADB")
        result = ADBAppManager.connect_device()
        return result
    except Exception as e:
        logger.error(f"Error connecting to device: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error connecting to device: {str(e)}")

# @app.post("/api/run_task")
# async def run_task(req: RunTaskRequest):
#     """
#     前端提交任务：通过包名、应用名和时间戳提交任务
#     后端会查找是否已有相同包名的任务，如果有则返回现有任务ID，否则创建新任务
#     """
#     try:
#         logger.info(f"Received run_task request - Package: {req.pkg}, App: {req.app}, Timestamp: {req.timestamp}")
        
#         # 查找是否已有该包名的任务
#         existing_task_id = task_manager.find_task_by_package(req.pkg)
        
#         if existing_task_id:
#             logger.info(f"Found existing task for package {req.pkg}: {existing_task_id}")
#             task_id = existing_task_id
#         else:
#             # 创建新任务
#             task_id = task_manager.submit_task(req.pkg, req.app, req.timestamp)
#             logger.info(f"Created new task - ID: {task_id}")
        
#         return {
#             "success": True,
#             "task_id": task_id,
#             "message": "Task submitted successfully"
#         }
        
#     except Exception as e:
#         logger.error(f"Error in run_task - Package: {req.pkg}, App: {req.app}, Error: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Task submission failed: {str(e)}")

# @app.post("/api/run_multiple_task")
@app.post("/api/run_task")
async def run_multiple_task(req: MultipleRunTaskRequest):
    """
    前端提交多个任务：通过包名、应用名和时间戳提交多个任务
    后端会查找是否已有相同包名的任务，如果有则返回现有任务ID，否则创建新任务
    处理过程是串行的
    """
    try:
        logger.info(f"Received run_multiple_task request - Total tasks: {len(req.tasks)}")
        
        results = []
        
        # 串行处理每个任务
        for idx, task_req in enumerate(req.tasks, 1):
            try:
                logger.info(f"Processing task {idx}/{len(req.tasks)} - Package: {task_req.pkg}, App: {task_req.app}, Timestamp: {task_req.timestamp}")
                
                # 查找是否已有该包名的任务
                existing_task_id = task_manager.find_task_by_package(task_req.pkg)
                
                if existing_task_id:
                    logger.info(f"Found existing task for package {task_req.pkg}: {existing_task_id}")
                    task_id = existing_task_id
                    is_new = False
                else:
                    # 创建新任务
                    task_id = task_manager.submit_task(task_req.pkg, task_req.app, task_req.timestamp)
                    logger.info(f"Created new task - ID: {task_id}")
                    is_new = True
                
                results.append({
                    "pkg": task_req.pkg,
                    "app": task_req.app,
                    "timestamp": task_req.timestamp,
                    "success": True,
                    "task_id": task_id,
                    "is_new": is_new,
                    "message": "Task submitted successfully"
                })
                
            except Exception as e:
                logger.error(f"Error in run_multiple_task task {idx}/{len(req.tasks)} - Package: {task_req.pkg}, App: {task_req.app}, Error: {str(e)}")
                results.append({
                    "pkg": task_req.pkg,
                    "app": task_req.app,
                    "timestamp": task_req.timestamp,
                    "success": False,
                    "task_id": None,
                    "message": f"Task submission failed: {str(e)}"
                })
        
        successful_count = len([r for r in results if r["success"]])
        logger.info(f"Multiple tasks processing completed - Total: {len(req.tasks)}, Successful: {successful_count}")
        
        return {
            "success": successful_count == len(req.tasks),
            "total": len(req.tasks),
            "successful": successful_count,
            "failed": len(req.tasks) - successful_count,
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Error in run_multiple_task - Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Multiple task submission failed: {str(e)}")

@app.get("/api/tasks")
async def check_task_completion(pkg: str):
    """
    查询指定包名的采集任务是否完成，返回简单的 true/false 状态
    """
    try:
        logger.info(f"Checking task completion for package: {pkg}")
        
        # 通过包名查找任务
        task_id = task_manager.find_task_by_package(pkg)
        
        if not task_id:
            logger.info(f"No task found for package: {pkg}")
            return False
        
        # 获取任务状态
        task_status = task_manager.get_status(task_id)
        status = task_status.get("status", "unknown")
        
        # 判断是否完成
        completed = status == "completed"
        
        logger.info(f"Task status for package {pkg}: {status}, completed: {completed}")
        
        return completed
        
    except Exception as e:
        logger.error(f"Error checking task completion for package {pkg}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error checking task status: {str(e)}")

##################################################
# 可选的其他 API 接口
##################################################

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

# @app.post("/api/run_multiple", response_model=dict)
# async def run_multiple_apps(req: MultipleTaskRequest):
#     """
#     接受多个 app 的数据收集请求，串行处理
#     """
#     try:
#         logger.info(f"Received multiple task request - Total apps: {len(req.apps)}")
        
#         task_ids = []
#         results = []
        
#         # 串行处理每个app
#         for idx, app_req in enumerate(req.apps, 1):
#             try:
#                 logger.info(f"Processing app {idx}/{len(req.apps)} - Package: {app_req.pkg}, App: {app_req.app}")
                
#                 task_id = task_manager.submit_task(app_req.pkg, app_req.app)
#                 task_ids.append(task_id)
                
#                 results.append({
#                     "pkg": app_req.pkg,
#                     "app": app_req.app,
#                     "task_id": task_id,
#                     "status": "success"
#                 })
                
#                 logger.info(f"Task {idx}/{len(req.apps)} submitted successfully - ID: {task_id}")
                
#             except Exception as e:
#                 logger.error(f"Error submitting task {idx}/{len(req.apps)} - Package: {app_req.pkg}, App: {app_req.app}, Error: {str(e)}")
#                 results.append({
#                     "pkg": app_req.pkg,
#                     "app": app_req.app,
#                     "task_id": None,
#                     "status": "failed",
#                     "error": str(e)
#                 })
        
#         logger.info(f"Multiple tasks processing completed - Total: {len(req.apps)}, Successful: {len([r for r in results if r['status'] == 'success'])}")
        
#         return {
#             "total": len(req.apps),
#             "successful": len([r for r in results if r['status'] == 'success']),
#             "failed": len([r for r in results if r['status'] == 'failed']),
#             "task_ids": task_ids,
#             "results": results
#         }
        
#     except Exception as e:
#         logger.error(f"Error in run_multiple_apps - Error: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Multiple task submission failed: {str(e)}")

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

@app.get("/api/list_tasks", response_model=dict)
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

@app.get("/api/download/{task_id}")
async def download_task_collected_data(task_id):
    """
    下载任务收集的数据
    """
    try:
        logger.info(f"Downloading task collected data - Task ID: {task_id}")
        data = task_manager.get_task_collected_data(task_id)
        return data
    except Exception as e:
        logger.error(f"Error downloading task collected data - Task ID: {task_id}, Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error downloading task collected data: {str(e)}")
