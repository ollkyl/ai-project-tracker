from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.db import models
from backend.app.db.session import get_db
from backend.app.schemas.task import TaskCreate, TaskOut

router = APIRouter()


@router.post("/", response_model=TaskOut)
def create_task(task: TaskCreate, project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    new_task = models.Task(title=task.title, status=task.status, project_id=project_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.put("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, status: str, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = status
    db.commit()
    db.refresh(task)
    return task
