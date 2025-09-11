from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from bot.services.api import create_idea

router = Router()


@router.message(Command("idea"))
async def cmd_idea(message: Message):
    idea_text = message.text.replace("/idea", "").strip()
    if not idea_text:
        await message.answer("✍️ Напиши идею после команды /idea")
        return

    try:
        idea = await create_idea(user_id=message.from_user.id, text=idea_text)
        await message.answer(
            f"✅ Идея сохранена!\n\n📌 {idea['title']}\n📝 {idea['description']}\n\nЗадачи:\n"
            + "\n".join([f"{i + 1}. {t['title']}" for i, t in enumerate(idea["tasks"])])
        )
    except Exception as e:
        await message.answer(f"❌ Ошибка сохранения идеи: {str(e)}")
