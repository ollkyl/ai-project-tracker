from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    model_config = ConfigDict(
        env_file="backend/.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str
    telegram_bot_token: str
    openai_api_key: Optional[str] = None
    admin_email: str
    admin_password: str
    backend_url: Optional[str] = "http://127.0.0.1:8000"


settings = Settings()
