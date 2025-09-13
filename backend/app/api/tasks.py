from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import models
from app.db.session import get_db
from app.schemas.task import TaskUpdate, TaskOut
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.patch("/{task_id}", response_model=TaskOut)
async def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    logger.info(f"Updating task: task_id={task_id}")
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        logger.warning(f"Task not found: task_id={task_id}")
        raise HTTPException(status_code=404, detail="Task not found")

    if task.status:
        db_task.status = task.status
    if task.progress is not None:
        db_task.progress = task.progress

    db.commit()
    db.refresh(db_task)
    logger.info(f"Task updated: task_id={task_id}, status={task.status}, progress={task.progress}")
    return db_task
