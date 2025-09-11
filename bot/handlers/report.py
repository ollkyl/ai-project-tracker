from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from bot.services.api import get_report

router = Router()


@router.message(Command("report"))
async def cmd_report(message: Message):
    try:
        report = await get_report(message.from_user.id)
        if not report:
            await message.answer("Нет проектов для отчёта 📊")
            return

        await message.answer(
            f"📊 Отчёт:\n\n Выполнено: {report['progress']}%\n🤖 AI совет: {report['advice']}"
        )
    except Exception as e:
        await message.answer(f" Ошибка получения отчёта: {str(e)}")
