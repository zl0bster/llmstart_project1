"""
Обработчики сообщений Telegram бота.
"""
from aiogram import types, Router
from aiogram.filters import Command
import logging
from llm_client import LLMClient

logger = logging.getLogger(__name__)

# Создаем роутер для обработчиков
router = Router()

# Инициализируем LLM клиент
llm_client = LLMClient()


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
    await message.reply("Привет! Я ИИ-помощник. Задай мне любой вопрос!")
    logger.info(f"Пользователь {message.from_user.id} запустил бота")


@router.message(Command("help"))
async def help_handler(message: types.Message):
    """Обработчик команды /help."""
    await message.reply("Доступные команды:\n/start - начать работу\n/help - справка\n\nПросто напишите мне любой вопрос!")
    logger.info(f"Пользователь {message.from_user.id} запросил справку")


@router.message()
async def text_handler(message: types.Message):
    """Обработчик всех текстовых сообщений через LLM."""
    if not message.text:
        return
    
    await message.reply("Думаю...")
    logger.info(f"Пользователь {message.from_user.id} отправил сообщение: {message.text}")
    
    answer = await llm_client.ask(message.text)
    
    if answer:
        await message.reply(answer)
        logger.info(f"LLM ответ для пользователя {message.from_user.id}: {answer[:100]}...")
    else:
        await message.reply("Извините, произошла ошибка при обработке запроса.")
        logger.error(f"Ошибка получения ответа от LLM для пользователя {message.from_user.id}")
