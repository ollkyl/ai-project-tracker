from aiogram import Router, types
from aiogram.filters import Command
import httpx
import logging
from bot.services.api import get_projects  # Импортируем get_projects для получения списка проектов

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("report"))
async def report_command(message: types.Message):
    try:
        args = message.text.replace("/report ", "").strip().split()

        if not args:
            await message.answer("Укажи номер проекта: /report номер_проекта")
            return

        project_number = args[0]

        # Получаем проекты пользователя
        projects = await get_projects(message.from_user.id)
        if not projects:
            await message.answer("У тебя пока нет проектов")
            return

        # Проверяем, что введённый номер валиден
        if (
            not project_number.isdigit()
            or int(project_number) < 1
            or int(project_number) > len(projects)
        ):
            await message.answer(f"Введи номер проекта от 1 до {len(projects)}")
            return

        # Преобразуем локальный номер в глобальный project_id
        project_id = projects[int(project_number) - 1]["id"]

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://127.0.0.1:8000/report/{project_id}?user_id={message.from_user.id}"
            )

            if response.status_code == 200:
                data = response.json()

                report_text = (
                    f"Отчёт: {data['project_title']} (ID: {project_id})\n\n"
                    f"✅ Выполнено: {data['completion_percentage']}% ({data['completed_tasks']}/{data['total_tasks']})\n\n"
                )

                report_text += "Подзадачи:\n"
                for i, task in enumerate(data["tasks"], 1):
                    task_title = task["title"]
                    # Убираем "1. ", "2. " если они есть в начале
                    if task_title.split(". ")[0].isdigit():
                        task_title = task_title.split(". ", 1)[1]
                    report_text += f"{i}. {task_title}\n"

                report_text += f"\nСовет:\n{data['ai_advice']}"

                await message.answer(report_text)
            else:
                await message.answer("Проект не найден")

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        await message.answer("Ошибка генерации отчёта.")
