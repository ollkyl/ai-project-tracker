from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.db import models
from backend.app.db.session import get_db
from backend.app.schemas.project import ProjectCreate, ProjectOut

router = APIRouter()


@router.post("/", response_model=ProjectOut)
def create_project(project: ProjectCreate, user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_project = models.Project(title=project.title, description=project.description, owner=user)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


@router.get("/", response_model=list[ProjectOut])
def get_projects(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Project).filter(models.Project.user_id == user_id).all()
