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
        'LOG_FILE': os.getenv('LOG_FILE', 'logs/bot.log'),
        # LLM настройки
        'OPENROUTER_API_KEY': os.getenv('OPENROUTER_API_KEY'),
        'OPENROUTER_API_URL': os.getenv('OPENROUTER_API_URL', 'https://openrouter.ai/api/v1'),
        'LLM_MODEL_NAME': os.getenv('LLM_MODEL_NAME', 'openai/gpt-3.5-turbo'),
        'LLM_TEMPERATURE': float(os.getenv('LLM_TEMPERATURE', '0.7')),
        'LLM_MAX_TOKENS': int(os.getenv('LLM_MAX_TOKENS', '500'))
    }
    
    # Валидация обязательных параметров
    if not config['TELEGRAM_BOT_TOKEN']:
        raise ValueError("TELEGRAM_BOT_TOKEN не найден в переменных окружения")
    
    if not config['OPENROUTER_API_KEY']:
        raise ValueError("OPENROUTER_API_KEY не найден в переменных окружения")
    
    return config
