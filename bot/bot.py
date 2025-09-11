import asyncio
import os
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from handlers.start import router as start_router
from handlers.idea import router as idea_router
from handlers.projects import router as projects_router
from handlers.update import router as update_router
from handlers.report import router as report_router
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def main():
    if not TOKEN:
        raise ValueError(" TELEGRAM_BOT_TOKEN не найден в .env")

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(idea_router)
    dp.include_router(projects_router)
    dp.include_router(update_router)
    dp.include_router(report_router)

    print("🤖 Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
