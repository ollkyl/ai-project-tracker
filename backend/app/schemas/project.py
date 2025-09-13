from pydantic import BaseModel
from typing import List, Optional
from app.schemas.task import TaskOut


class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectOut(ProjectBase):
    id: int
    tasks: List[TaskOut] = []

    class Config:
        orm_mode = True
