"""
Конфигурация CRM-бота.
Загружает настройки из переменных окружения.
"""

import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()


# Telegram Bot
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Database (Neon PostgreSQL)
DATABASE_URL = os.getenv("DATABASE_URL")

# Альтернативный вариант с отдельными параметрами
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def get_db_connection_string() -> str:
    """
    Возвращает строку подключения к базе данных.
    Приоритет: DATABASE_URL, иначе собирается из отдельных параметров.
    """
    if DATABASE_URL:
        return DATABASE_URL
    
    if all([DB_HOST, DB_NAME, DB_USER, DB_PASSWORD]):
        return f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    raise ValueError(
        "Не заданы параметры подключения к БД. "
        "Укажите DATABASE_URL или DB_HOST, DB_NAME, DB_USER, DB_PASSWORD"
    )

