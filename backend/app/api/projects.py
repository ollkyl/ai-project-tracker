from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from backend.app.db import models
from backend.app.db.session import get_db
from backend.app.schemas.project import ProjectOut

router = APIRouter()


@router.get("/", response_model=list[ProjectOut])
def get_projects(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.telegram_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Загружаем проекты с задачами
    projects = (
        db.query(models.Project)
        .options(joinedload(models.Project.tasks))
        .filter(models.Project.user_id == user.id)
        .all()
    )

    return projects


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.telegram_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    project = (
        db.query(models.Project)
        .filter(models.Project.id == project_id, models.Project.user_id == user.id)
        .first()
    )

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project
