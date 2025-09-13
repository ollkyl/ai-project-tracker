from app.db.session import engine, Base
from app.db.models import *
import logging
import time

# Настройка логирования для отладки
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_all_tables():
    """
    Создает все таблицы в базе данных, используя синхронный подход.
    """
    logger.info("Attempting to connect to the database...")
    # Добавляем небольшой таймаут, чтобы дать PostgreSQL время на полный запуск
    time.sleep(5)
    try:
        # Синхронный вызов для создания таблиц
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully.")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        # Переброс исключения, чтобы остановить контейнер в случае неудачи
        raise


if __name__ == "__main__":
    create_all_tables()
