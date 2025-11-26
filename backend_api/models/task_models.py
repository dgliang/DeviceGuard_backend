from pydantic import BaseModel

class TaskRequest(BaseModel):
    pkg: str
    app: str

class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    progress: float
    message: str
