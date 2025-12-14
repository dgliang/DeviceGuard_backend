from pydantic import BaseModel
from typing import List

class TaskRequest(BaseModel):
    pkg: str
    app: str

class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    progress: float
    message: str

class RunTaskRequest(BaseModel):
    pkg: str
    app: str
    timestamp: str

class MultipleTaskRequest(BaseModel):
    apps: List[TaskRequest]

class MultipleRunTaskRequest(BaseModel):
    tasks: List[RunTaskRequest]
