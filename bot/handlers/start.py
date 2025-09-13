from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
import re
import aiohttp
from services.api import register_user

router = Router()


API_URL = "http://backend:8000/users/"


async def get_user_by_telegram_id(telegram_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}?telegram_id={telegram_id}") as resp:
            if resp.status == 200:
                data = await resp.json()
                if data:
                    return data[0] if isinstance(data, list) else data
            elif resp.status == 404:
                return None
            else:
                raise Exception(f"Ошибка сервера: {resp.status}")
    return None


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Добро пожаловать! "
        "Гайд по команде: /help\n\n"
        "Введите своё имя и email через пробел (например: Иван ivan@mail.com)"
    )


@router.message(Command(commands=["help"]))
async def cmd_help(message: Message):
    await message.answer(
        "Гайд по использованию:\n"
        "- Чтобы зарегистрироваться, введите имя и email через пробел, например: Иван ivan@mail.com\n"
        "- Используйте /start чтобы увидеть приветствие снова"
    )


@router.message(
    lambda message: bool(
        re.match(
            r"^[a-zA-Zа-яА-Я\s\-]+\s+[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            message.text,
        )
    )
)
async def register(message: Message):
    parts = message.text.split(maxsplit=1)
    name, email = parts

    try:
        # Проверяем, зарегистрирован ли уже Telegram ID
        existing_user = await get_user_by_telegram_id(message.from_user.id)
        if existing_user:
            await message.answer(
                f"Ты уже зарегистрирован!\nИмя: {existing_user['name']}\nEmail: {existing_user['email']}"
            )
            return

        # Если не зарегистрирован, создаём нового
        user = await register_user(name, email, message.from_user.id)
        await message.answer(f"Ты зарегистрирован!\nИмя: {name}\nEmail: {email}")

    except Exception as e:
        await message.answer(f"Ошибка регистрации: {str(e)}")
