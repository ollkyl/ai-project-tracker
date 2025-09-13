from apscheduler.schedulers.asyncio import AsyncIOScheduler
import httpx
import logging
from aiogram import Bot
from bot.services.api import BASE_URL
from backend.app.core.config import settings

logger = logging.getLogger(__name__)


async def get_general_advice(total_completed: int, total_tasks: int, project_titles: list) -> str:
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

        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.post(
                settings.gemini_api_url,
                headers={
                    "Content-Type": "application/json",
                    "X-goog-api-key": settings.gemini_api_key,
                },
                json={"contents": [{"parts": [{"text": prompt}]}]},
                timeout=10.0,
            )
            response.raise_for_status()
            advice = response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
            return advice
    except httpx.HTTPError as e:
        logger.error(f"Gemini API error: {str(e)}")
        return "Общий совет: Продолжай работать над задачами."


async def send_status_updates(bot: Bot):
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.get(f"{BASE_URL}/users/", timeout=10.0)
            response.raise_for_status()
            users = response.json()
        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch users from {BASE_URL}/users/: {str(e)}")
            return

        for user in users:
            telegram_id = user["telegram_id"]
            try:
                report_response = await client.get(
                    f"{BASE_URL}/report?user_id={telegram_id}", timeout=10.0
                )
                report_response.raise_for_status()
                data = report_response.json()
            except httpx.HTTPError as e:
                logger.warning(f"Failed to get report for user {telegram_id}: {str(e)}")
                continue

            projects = data.get("projects", [])
            if not projects:
                continue

            total_completed = sum(project["completed_tasks"] for project in projects)
            total_tasks = sum(project["total_tasks"] for project in projects)
            project_titles = [project["project_title"] for project in projects]

            message_text = "📊 Ежедневный статус-апдейт по твоим проектам:\n\n"
            for i, project in enumerate(projects, 1):
                message_text += (
                    f"{i}. {project['project_title']} (ID: {project['project_id']})\n"
                    f"✅ Выполнено: {project['completion_percentage']}% "
                    f"({project['completed_tasks']}/{project['total_tasks']})\n\n"
                )

            try:
                message_text += await get_general_advice(
                    total_completed, total_tasks, project_titles
                )
                await bot.send_message(chat_id=telegram_id, text=message_text, parse_mode="HTML")
            except Exception as e:
                logger.error(f"Failed to send message to {telegram_id}: {str(e)}")


def setup_scheduler(bot: Bot):
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(send_status_updates, trigger="interval", minutes=10, args=[bot])
    scheduler.start()
    logger.info("Scheduler started")
