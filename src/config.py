"""
Конфигурация приложения.
Загружает настройки из переменных окружения.
"""
import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()


def get_config():
    """
    Получить конфигурацию приложения.
    
    Returns:
        dict: Словарь с настройками приложения
    """
    config = {
        'TELEGRAM_BOT_TOKEN': os.getenv('TELEGRAM_BOT_TOKEN'),
        'LOG_LEVEL': os.getenv('LOG_LEVEL', 'INFO'),
        'LOG_FILE': os.getenv('LOG_FILE', 'logs/bot.log')
    }
    
    # Валидация обязательных параметров
    if not config['TELEGRAM_BOT_TOKEN']:
        raise ValueError("TELEGRAM_BOT_TOKEN не найден в переменных окружения")
    
    return config
