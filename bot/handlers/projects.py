from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from bot.services.api import get_projects

router = Router()


@router.message(Command("projects"))
async def cmd_projects(message: Message):
    try:
        projects = await get_projects(message.from_user.id)
        if not projects:
            await message.answer("У тебя пока нет проектов")
            return

        text = "Проекты:\n\n"
        for i, project in enumerate(projects, 1):
            text += f"{i}. {project['title']} \n"

        await message.answer(text)
    except Exception as e:
        await message.answer(f"Ошибка получения проектов: {str(e)}")
