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



def validate_config() -> bool:
    """
    Проверяет, что все необходимые настройки заданы корректно.
    Возвращает True, если конфигурация валидна, иначе False.
    """
    errors = []
    warnings = []
    
    # Проверка BOT_TOKEN
    if not BOT_TOKEN:
        errors.append("❌ BOT_TOKEN не задан в файле .env")
    elif len(BOT_TOKEN) < 30:
        warnings.append("⚠️  BOT_TOKEN слишком короткий (возможно, неверный токен)")
    
    # Проверка подключения к БД
    try:
        db_url = get_db_connection_string()
        if not db_url:
            errors.append("❌ Не задана строка подключения к базе данных")
        else:
            # Проверка формата URL
            if not db_url.startswith("postgresql://"):
                warnings.append("⚠️  Строка подключения должна начинаться с 'postgresql://'")
            
            # Проверка локального подключения
            if "localhost" in db_url or "127.0.0.1" in db_url:
                print("ℹ️  Используется локальная база данных PostgreSQL")
            elif "neon.tech" in db_url:
                warnings.append("⚠️  Обнаружена Neon.tech. Убедитесь, что сервис доступен в вашем регионе")
                
    except ValueError as e:
        errors.append(f"❌ Ошибка в настройках БД: {e}")
    
    # Вывод результатов
    if errors:
        print("\n❌ ОШИБКИ КОНФИГУРАЦИИ:")
        for error in errors:
            print(f"  {error}")
    
    if warnings:
        print("\n⚠️  ПРЕДУПРЕЖДЕНИЯ:")
        for warning in warnings:
            print(f"  {warning}")
    
    if not errors and not warnings:
        print("\n✅ Конфигурация проверена успешно!")
        print(f"   Бот: @{BOT_TOKEN[:10]}... (токен скрыт)")
        print(f"   БД: {get_db_connection_string()}")
        return True
    
    if errors:
        print("\n❌ Исправьте ошибки перед запуском бота")
        return False
    
    # Есть только предупреждения, но нет ошибок
    print("\n⚠️  Конфигурация работает, но есть предупреждения")
    return True


def get_config_info() -> dict:
    """
    Возвращает словарь с информацией о конфигурации (без敏感 данных).
    Полезно для логирования и отладки.
    """
    db_url = get_db_connection_string() if DATABASE_URL or all([DB_HOST, DB_NAME, DB_USER, DB_PASSWORD]) else None
    
    # Скрываем пароль в строке подключения для безопасности
    if db_url:
        # Простая маскировка пароля
        import re
        db_url_masked = re.sub(r':([^:@]+)@', r':***@', db_url)
    else:
        db_url_masked = None
    
    return {
        "bot_token_set": bool(BOT_TOKEN),
        "bot_token_preview": f"{BOT_TOKEN[:10]}..." if BOT_TOKEN else None,
        "database_url_set": bool(DATABASE_URL),
        "database_url_masked": db_url_masked,
        "db_host": DB_HOST,
        "db_name": DB_NAME,
        "db_user": DB_USER,
        "db_port": DB_PORT,
        "is_local_db": bool(db_url and ("localhost" in db_url or "127.0.0.1" in db_url))
    }


# Автоматическая проверка при импорте (можно закомментировать, если не нужно)
if __name__ == "__main__":
    print("=" * 50)
    print("ПРОВЕРКА КОНФИГУРАЦИИ CRM БОТА")
    print("=" * 50)
    validate_config()
    print("\nДЕТАЛИ КОНФИГУРАЦИИ:")
    info = get_config_info()
    for key, value in info.items():
        print(f"  {key}: {value}")
