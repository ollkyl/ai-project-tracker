from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    title: str
    status: str = "todo"
    progress: int = 0


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    status: Optional[str] = None
    progress: Optional[int] = None


class TaskOut(TaskBase):
    id: int
    project_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
