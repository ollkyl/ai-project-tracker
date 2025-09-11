from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from services.api import register_user

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Введи своё имя и email через пробел (например: Иван ivan@mail.com)"
    )


@router.message()
async def register(message: Message):
    parts = message.text.split()
    if len(parts) == 2:
        name, email = parts
        user = await register_user(name, email, message.from_user.id)
        await message.answer(f"✅ Ты зарегистрирован!\nИмя: {name}\nEmail: {email}")
    else:
        await message.answer("❌ Формат неправильный. Попробуй снова: Имя email")
