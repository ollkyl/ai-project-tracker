from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.db import models
from backend.app.db.session import get_db
from backend.app.core.config import settings
import openai

router = APIRouter()

openai.api_key = settings.openai_api_key


@router.get("/")
async def get_report(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.telegram_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    projects = db.query(models.Project).filter(models.Project.user_id == user.id).all()
    if not projects:
        return {}

    total_tasks = 0
    done_tasks = 0
    project_summaries = []
    for project in projects:
        tasks = db.query(models.Task).filter(models.Task.project_id == project.id).all()
        total_tasks += len(tasks)
        done_tasks += len([t for t in tasks if t.status == "done"])
        project_summaries.append(
            f"Проект '{project.title}': {len([t for t in tasks if t.status == 'done'])}/{len(tasks)} задач выполнено"
        )

    progress = (done_tasks / total_tasks * 100) if total_tasks > 0 else 0

    if settings.openai_api_key:
        prompt = f"Пользователь завершил {done_tasks} из {total_tasks} задач. Проекты: {'; '.join(project_summaries)}. Дай совет, что мешает прогрессу и как двигаться дальше."
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
            )
            advice = response.choices[0].message.content
        except Exception:
            advice = "Продолжайте работать над задачами!"
    else:
        advice = "Продолжайте работать над задачами!"

    return {"progress": round(progress, 2), "advice": advice}
