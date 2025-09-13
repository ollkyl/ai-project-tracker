from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging
from aiogram import Bot
from services.api import get_all_users, get_projects, get_general_advice


logger = logging.getLogger(__name__)


async def send_status_updates(bot: Bot):
    try:
        users = await get_all_users()
    except Exception as e:
        logger.error(f"Failed to fetch users: {str(e)}")
        return

    for user in users:
        telegram_id = user["telegram_id"]
        try:
            projects = await get_projects(telegram_id)
            if not projects:
                continue

            message_text = "📊 Ежедневный статус-апдейт по твоим проектам:\n\n"
            for i, project in enumerate(projects, 1):
                project_tasks = project.get("tasks", [])
                project_completed = sum(1 for task in project_tasks if task["status"] == "done")
                project_total = len(project_tasks)
                completion_percentage = (
                    (project_completed / project_total * 100) if project_total > 0 else 0.0
                )
                message_text += (
                    f"{i}. {project['title']} (ID: {project['id']})\n"
                    f"✅ Выполнено: {round(completion_percentage, 1)}% "
                    f"({project_completed}/{project_total})\n\n"
                )

            advice_data = await get_general_advice(telegram_id)
            general_advice = advice_data.get(
                "general_advice", "Общий совет: Продолжай работать над задачами."
            )
            message_text += general_advice

            await bot.send_message(chat_id=telegram_id, text=message_text, parse_mode="HTML")
        except Exception as e:
            logger.error(f"Failed to process or send for user {telegram_id}: {str(e)}")


def setup_scheduler(bot: Bot):
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(send_status_updates, trigger="interval", minutes=10, args=[bot])
    scheduler.start()
    logger.info("Scheduler started")
