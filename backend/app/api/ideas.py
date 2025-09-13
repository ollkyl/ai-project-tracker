from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import cast
from sqlalchemy.sql.sqltypes import BigInteger
from app.db import models
from app.db.session import get_db
from app.schemas.project import ProjectOut
from app.core.config import settings
import httpx
import logging
import json
import re

router = APIRouter()
logger = logging.getLogger(__name__)


async def generate_roadmap_with_gemini(idea_text: str) -> list:
    """Генерация roadmap с помощью Google Gemini"""
    try:
        prompt = f"""
        Пользователь предложил идею: "{idea_text}".
        Сгенерируй roadmap из 5 конкретных, измеримых и реалистичных задач для реализации этой идеи.
        Задачи должны быть последовательными и практичными.
        
        Верни ТОЛЬКО валидный JSON массив строк в формате: ["Задача 1", "Задача 2", ...]
        Не добавляй никаких дополнительных комментариев или объяснений.
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
                    "generationConfig": {"temperature": 0.7, "maxOutputTokens": 500},
                },
                timeout=30.0,
            )

            response.raise_for_status()
            data = response.json()

            # Извлекаем текст из ответа Gemini
            ai_text = data["candidates"][0]["content"]["parts"][0]["text"]

            # Очистка ответа от markdown и лишних символов
            ai_text = re.sub(r"```json|```", "", ai_text).strip()

            tasks = json.loads(ai_text)

            if not isinstance(tasks, list) or len(tasks) == 0:
                raise ValueError("Invalid tasks format from AI")

            return tasks[:5]  # Максимум 5 задач

    except Exception as e:
        logger.error(f"Gemini roadmap generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI generation error: {str(e)}")


@router.post("/", response_model=ProjectOut)
async def create_idea(text: str, user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Creating idea: text={text}, user_id={user_id}")

    user = (
        db.query(models.User).filter(models.User.telegram_id == cast(user_id, BigInteger)).first()
    )
    if not user:
        logger.warning(f"User not found: user_id={user_id}")
        raise HTTPException(status_code=404, detail="User not found")

    # ПРОВЕРКА ДУБЛИКАТОВ - если проект с таким названием уже есть
    existing_project = (
        db.query(models.Project)
        .filter(models.Project.title == text, models.Project.user_id == user.id)
        .first()
    )

    if existing_project:
        logger.info(f"Using existing project: {text}")
        return existing_project

    # Генерация roadmap с помощью Gemini
    try:
        tasks = await generate_roadmap_with_gemini(text)
        logger.info(f"Successfully generated roadmap with Gemini: {len(tasks)} tasks")
    except Exception as e:
        logger.error(f"Gemini generation completely failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail="AI service unavailable. Please try again later."
        )

    description = f"AI-сгенерированный проект на основе идеи: {text}"

    # Создание проекта
    new_project = models.Project(title=text[:100], description=description, user_id=user.id)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    # Создание задач (без добавления номеров в названия)
    for i, task_title in enumerate(tasks, 1):
        # Сохраняем задачи без префиксов "1. ", "2. " в базе
        clean_title = task_title
        if task_title.startswith(f"{i}. "):
            clean_title = task_title[len(f"{i}. ") :]

        new_task = models.Task(
            title=clean_title[:200], status="todo", progress=0, project_id=new_project.id
        )
        db.add(new_task)

    db.commit()
    db.refresh(new_project)

    logger.info(f"Idea created: {text} with {len(tasks)} tasks for user_id={user_id}")
    return new_project
