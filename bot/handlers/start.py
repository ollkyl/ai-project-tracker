from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
import re
from bot.services.api import register_user

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Добро пожаловть! "
        "Гайд по команде: /help\n\n"
        "Введите своё имя и email через пробел (например: Иван ivan@mail.com)"
    )


@router.message(
    lambda message: bool(
        re.match(
            r"^[a-zA-Zа-яА-Я]+\s+[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", message.text
        )
    )
)
async def register(message: Message):
    parts = message.text.split()
    name, email = parts
    try:
        user = await register_user(name, email, message.from_user.id)
        await message.answer(f" Ты зарегистрирован!\nИмя: {name}\nEmail: {email}")
    except Exception as e:
        await message.answer(f" Ошибка регистрации: {str(e)}")
