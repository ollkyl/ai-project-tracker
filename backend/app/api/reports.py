from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import cast
from sqlalchemy.sql.sqltypes import BigInteger
from backend.app.db import models
from backend.app.db.session import get_db
from backend.app.core.config import settings
import httpx
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


async def get_gemini_analysis(
    completed_tasks: int, total_tasks: int, completion_percentage: float, project_title: str
) -> str:
    """Генерация AI анализа с помощью Gemini для конкретного проекта"""
    try:
        prompt = f"""
            Анализ прогресса проекта: "{project_title}"
            - Выполнено задач: {completed_tasks} из {total_tasks} ({completion_percentage:.1f}%)

            Сформируй ответ строго в формате:

            Идея "{project_title}" ... (анализ прогресса в 1–2 предложениях)

            Рекомендации:
                * 
                * 
                * 

            Короткая мотивация (1 предложение).

            Будь конкретным, практичным и мотивирующим. Ответ не более 80 слов.
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
                timeout=30.0,
            )

            response.raise_for_status()
            data = response.json()

            return data["candidates"][0]["content"]["parts"][0]["text"].strip()

    except Exception as e:
        logger.error(f"Gemini analysis failed: {str(e)}")
        return "Анализ временно недоступен. Продолжайте работать над задачами!"


@router.get("/")
async def get_report(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Generating report for user_id={user_id}")

    user = (
        db.query(models.User).filter(models.User.telegram_id == cast(user_id, BigInteger)).first()
    )
    if not user:
        logger.warning(f"User not found: user_id={user_id}")
        raise HTTPException(status_code=404, detail="User not found")

    report_data = []

    for project in user.projects:
        total_tasks = len(project.tasks)
        completed_tasks = sum(1 for task in project.tasks if task.status == "done")
        completion_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0.0

        # Генерация AI анализа для каждого проекта
        ai_advice = await get_gemini_analysis(
            completed_tasks, total_tasks, completion_percentage, project.title
        )

        report_data.append(
            {
                "project_id": project.id,
                "project_title": project.title,
                "completed_tasks": completed_tasks,
                "total_tasks": total_tasks,
                "completion_percentage": round(completion_percentage, 1),
                "ai_advice": ai_advice,
                "tasks": [
                    {
                        "id": task.id,
                        "title": task.title,
                        "status": task.status,
                        "progress": task.progress,
                    }
                    for task in project.tasks
                ],
            }
        )

    return {"projects": report_data}


# НОВЫЙ ENDPOINT ДЛЯ ОТЧЁТА ПО КОНКРЕТНОМУ ПРОЕКТУ
@router.get("/{project_id}")
async def get_project_report(project_id: int, user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Generating report for project_id={project_id}, user_id={user_id}")

    user = (
        db.query(models.User).filter(models.User.telegram_id == cast(user_id, BigInteger)).first()
    )
    if not user:
        logger.warning(f"User not found: user_id={user_id}")
        raise HTTPException(status_code=404, detail="User not found")

    project = (
        db.query(models.Project)
        .filter(models.Project.id == project_id, models.Project.user_id == user.id)
        .first()
    )

    if not project:
        logger.warning(f"Project not found: project_id={project_id}")
        raise HTTPException(status_code=404, detail="Project not found")

    total_tasks = len(project.tasks)
    completed_tasks = sum(1 for task in project.tasks if task.status == "done")
    completion_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0.0

    # Генерация AI анализа
    ai_advice = await get_gemini_analysis(
        completed_tasks, total_tasks, completion_percentage, project.title
    )

    return {
        "project_id": project.id,
        "project_title": project.title,
        "completed_tasks": completed_tasks,
        "total_tasks": total_tasks,
        "completion_percentage": round(completion_percentage, 1),
        "ai_advice": ai_advice,
        "tasks": [
            {
                "id": task.id,
                "title": task.title,
                "status": task.status,
                "progress": task.progress,
            }
            for task in project.tasks
        ],
    }
