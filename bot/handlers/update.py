from aiogram import Router, types
from aiogram.filters import Command
import httpx
import logging
from bot.services.api import get_projects  # Импортируем get_projects

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("update"))
async def update_command(message: types.Message):
    try:
        args = message.text.replace("/update ", "").strip().split()

        if len(args) != 2:
            await message.answer(
                "Формат: /update номер_проекта номер_пункта (например: /update 2 1)"
            )
            return

        project_number, task_number = args

        # Получаем проекты пользователя
        projects = await get_projects(message.from_user.id)
        if not projects:
            await message.answer("У тебя пока нет проектов")
            return

        # Проверяем, что введённый номер проекта валиден
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
            # Получаем проект
            project_response = await client.get(
                f"http://127.0.0.1:8000/projects/{project_id}?user_id={message.from_user.id}"
            )

            if project_response.status_code != 200:
                await message.answer("Проект не найден")
                return

            project_data = project_response.json()
            tasks = project_data.get("tasks", [])

            # Проверяем, что введённый номер задачи валиден
            if not tasks or int(task_number) > len(tasks) or int(task_number) < 1:
                await message.answer(f"В проекте только {len(tasks)} пунктов")
                return

            task = tasks[int(task_number) - 1]  # -1 потому что нумерация с 1

            # Обновляем задачу - меняем статус на "done"
            update_response = await client.patch(
                f"http://127.0.0.1:8000/tasks/{task['id']}", json={"status": "done"}
            )

            if update_response.status_code == 200:
                await message.answer(f"✅ Пункт {task_number} отмечен как выполненный!")
            else:
                await message.answer(f"Ошибка при обновлении: {update_response.text}")

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        await message.answer(f"Ошибка: {str(e)}")
