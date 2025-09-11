from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from services.api import update_task

router = Router()


@router.message(Command("update"))
async def cmd_update(message: Message):
    parts = message.text.split()
    if len(parts) < 3:
        await message.answer("Формат: /update <id задачи> <статус>")
        return

    task_id, status = parts[1], parts[2]
    updated = await update_task(task_id, status)
    if updated:
        await message.answer(f"✅ Статус задачи {task_id} обновлён на {status}")
    else:
        await message.answer("❌ Ошибка при обновлении")
