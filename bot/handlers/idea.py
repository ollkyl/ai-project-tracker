from aiogram import Router, types
from aiogram.filters import Command
import httpx
import logging

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("idea"))
async def idea_command(message: types.Message):
    try:
        idea_text = message.text.replace("/idea ", "").strip()
        if not idea_text:
            await message.answer("Укажи идею после /idea")
            return

        logger.info(f"Sending idea: {idea_text}, user_id={message.from_user.id}")
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://backend:8000/ideas/",
                params={"text": idea_text, "user_id": message.from_user.id},
            )

            if response.status_code == 200:
                project_data = response.json()
                tasks = project_data.get("tasks", [])

                response_text = f"✅ Идея сохранена: {idea_text}\n\nПодзадачи:\n"

                for i, task in enumerate(tasks, 1):
                    task_title = task["title"]
                    # Убираем "1. ", "2. " если они есть в начале
                    if task_title.split(". ")[0].isdigit():
                        task_title = task_title.split(". ", 1)[1]
                    response_text += f"{i}. {task_title}\n"

                await message.answer(response_text)
            else:
                await message.answer(f"Ошибка: {response.text}")

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        await message.answer(f"Ошибка: {str(e)}")
