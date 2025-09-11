from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.db import models
from backend.app.db.session import get_db
from backend.app.schemas.project import ProjectCreate, ProjectOut
from backend.app.schemas.task import TaskCreate
from backend.app.core.config import settings
import openai
import json

router = APIRouter()

openai.api_key = settings.openai_api_key


@router.post("/", response_model=ProjectOut)
async def create_idea(text: str, user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.telegram_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # AI-запрос
    if settings.openai_api_key:
        prompt = f"Сгенерируй описание для идеи: '{text}'. Также создай roadmap из 5–7 задач. Верни JSON с полями 'description' и 'tasks' (список строк)."
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
            )
            ai_result = response.choices[0].message.content
            ai_data = json.loads(ai_result)
            description = ai_data.get("description", text)
            tasks = ai_data.get("tasks", [])
        except Exception as e:
            description = text
            tasks = ["Задача 1", "Задача 2", "Задача 3", "Задача 4", "Задача 5"]
    else:
        description = text
        tasks = ["Задача 1", "Задача 2", "Задача 3", "Задача 4", "Задача 5"]

    # Создаём проект
    new_project = models.Project(title=text, description=description, user_id=user.id)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    # Создаём задачи
    for task_title in tasks:
        new_task = models.Task(title=task_title, status="todo", project_id=new_project.id)
        db.add(new_task)
    db.commit()

    return new_project
