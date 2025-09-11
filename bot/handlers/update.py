from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from bot.services.api import update_task

router = Router()


@router.message(Command("update"))
async def cmd_update(message: Message):
    parts = message.text.split()
    if len(parts) < 3:
        await message.answer("Формат: /update <id задачи> <статус>")
        return

    task_id, status = parts[1], parts[2]
    try:
        updated = await update_task(task_id, status)
        await message.answer(f"✅ Статус задачи {task_id} обновлён на {status}")
    except Exception as e:
        await message.answer(f"❌ Ошибка при обновлении: {str(e)}")
