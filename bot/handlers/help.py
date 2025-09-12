from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("help"))
async def help_command(message: types.Message):
    print("✅ HELP COMMAND TRIGGERED!")  # ← Добавьте эту строку
    help_text = """
🤖 <b>AI Project Tracker - Полная инструкция</b>

<b>Перед началом:</b>
*Перед началом:*
1. Используйте `/start` для регистрации
2. Введите имя и email (например: `Иван ivan@mail.com`)

*Основные команды после регистрации:*
💡 `/idea [ваша идея]` - Создать проект
📂 `/projects` - Показать все проекты с ID
✅ `/update [ID] [номер]` - Отметить пункт выполненным
📊 `/report [ID]` - Отчёт по проекту
❓ `/help` - Эта инструкция

*Пример:*
/idea выучить английский
/projects → запоминаем ID 
/update 1 1 → отмечаем первый шаг
/report 1 → смотрим прогресс

💡 Начинайте с маленьких идей!
    
"""
    await message.answer(help_text)
