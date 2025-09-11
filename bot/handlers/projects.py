from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from services.api import get_projects

router = Router()


@router.message(Command("projects"))
async def cmd_projects(message: Message):
    projects = await get_projects(message.from_user.id)
    if not projects:
        await message.answer("У тебя пока нет проектов 🚀")
        return

    text = "📂 Твои проекты:\n\n"
    for p in projects:
        text += f"— {p['title']} (id: {p['id']})\n"
    await message.answer(text)
