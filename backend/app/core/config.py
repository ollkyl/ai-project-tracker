from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL")
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "your_telegram_bot_token_here")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "your_gemini_api_key_here")
    gemini_api_url: str = os.getenv(
        "GEMINI_API_URL",
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
    )
    backend_url: str = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
