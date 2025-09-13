from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql.expression import cast
from sqlalchemy.sql.sqltypes import BigInteger
from app.db import models
from app.db.session import get_db
from app.core.config import settings
import httpx
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


async def get_general_gemini_advice(
    total_completed: int, total_tasks: int, project_titles: list
) -> str:
    try:
        completion_percentage = (total_completed / total_tasks * 100) if total_tasks > 0 else 0.0
        prompt = f"""
        Пользователь имеет проекты: {", ".join(project_titles)}.
        Всего задач: {total_tasks}, выполнено: {total_completed} ({completion_percentage:.1f}%).
        Дай общий совет:
        Общий совет: ... (1-2 предложения)
        Рекомендации:
            * ...
            * ...
            * ...
        Мотивация: ... (1 предложение)
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                settings.gemini_api_url,
                headers={
                    "Content-Type": "application/json",
                    "X-goog-api-key": settings.gemini_api_key,
                },
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"temperature": 0.8, "maxOutputTokens": 150},
                },
                timeout=10.0,
            )
            response.raise_for_status()
            return response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        logger.error(f"General Gemini advice failed: {str(e)}")
        return "Общий совет: Продолжай работать над задачами."


@router.get("/")
async def get_general_advice(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Generating general advice for user_id={user_id}")
    user = (
        db.query(models.User)
        .options(joinedload(models.User.projects).joinedload(models.Project.tasks))
        .filter(models.User.telegram_id == cast(user_id, BigInteger))
        .first()
    )
    if not user:
        logger.warning(f"User not found: user_id={user_id}")
        raise HTTPException(status_code=404, detail="User not found")

    total_completed = 0
    total_tasks = 0
    project_titles = []
    for project in user.projects:
        project_total_tasks = len(project.tasks)
        project_completed_tasks = sum(1 for task in project.tasks if task.status == "done")
        total_tasks += project_total_tasks
        total_completed += project_completed_tasks
        project_titles.append(project.title)

    general_advice = await get_general_gemini_advice(total_completed, total_tasks, project_titles)
    return {
        "total_completed": total_completed,
        "total_tasks": total_tasks,
        "general_advice": general_advice,
    }
