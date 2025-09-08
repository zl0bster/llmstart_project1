"""
Точка входа Telegram бота.
"""
import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import get_config
from handlers import register_handlers


def setup_logging():
    """Настройка логирования."""
    config = get_config()
    
    # Создаем директорию для логов если её нет
    import os
    os.makedirs(os.path.dirname(config['LOG_FILE']), exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, config['LOG_LEVEL']),
        format='%(asctime)s %(levelname)s %(name)s: %(message)s',
        handlers=[
            logging.FileHandler(config['LOG_FILE'], encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Логирование настроено")


def main():
    """Главная функция запуска бота."""
    try:
        # Настройка логирования
        setup_logging()
        logger = logging.getLogger(__name__)
        
        # Загрузка конфигурации
        config = get_config()
        logger.info("Конфигурация загружена")
        
        # Создание бота и диспетчера
        bot = Bot(token=config['TELEGRAM_BOT_TOKEN'])
        dp = Dispatcher(storage=MemoryStorage())
        
        # Регистрация обработчиков
        register_handlers(dp)
        logger.info("Обработчики зарегистрированы")
        
        # Запуск бота
        logger.info("Бот запущен")
        asyncio.run(dp.start_polling(bot))
        
    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")
        raise


if __name__ == '__main__':
    main()
