"""
Обработчики сообщений Telegram бота.
"""
from aiogram import types, Router
from aiogram.filters import Command
import logging

logger = logging.getLogger(__name__)

# Создаем роутер для обработчиков
router = Router()


def register_handlers(dp):
    """
    Регистрирует обработчики сообщений.
    
    Args:
        dp: Диспетчер aiogram
    """
    dp.include_router(router)


@router.message(Command("start"))
async def start_handler(message: types.Message):
    """Обработчик команды /start."""
    await message.reply("Привет! Я эхо-бот. Отправь мне любое сообщение.")
    logger.info(f"Пользователь {message.from_user.id} запустил бота")


@router.message(Command("help"))
async def help_handler(message: types.Message):
    """Обработчик команды /help."""
    await message.reply("Доступные команды:\n/start - начать работу\n/help - справка")
    logger.info(f"Пользователь {message.from_user.id} запросил справку")


@router.message()
async def echo_handler(message: types.Message):
    """Обработчик текстовых сообщений (эхо)."""
    await message.reply(message.text)
    logger.info(f"Эхо: {message.text} от пользователя {message.from_user.id}")
