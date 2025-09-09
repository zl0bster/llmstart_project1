"""
Обработчики сообщений Telegram бота.
"""
from aiogram import types, Router
from aiogram.filters import Command
import logging
from datetime import datetime
from typing import Dict, List
from llm_client import LLMClient

logger = logging.getLogger(__name__)

# Создаем роутер для обработчиков
router = Router()

# Инициализируем LLM клиент
llm_client = LLMClient()

# Хранение истории диалогов в памяти по chat_id
chat_history: Dict[int, List[Dict]] = {}


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
    await message.reply("Доступные команды:\n/start - начать работу\n/help - справка\n/reset - очистить историю диалога\n\nПросто напишите мне любой вопрос!")
    logger.info(f"Пользователь {message.from_user.id} запросил справку")


@router.message(Command("reset"))
async def reset_handler(message: types.Message):
    """Обработчик команды /reset - очистка истории диалога."""
    chat_id = message.chat.id
    
    if chat_id in chat_history:
        del chat_history[chat_id]
        await message.reply("История диалога очищена.")
        logger.info(f"История диалога очищена для пользователя {message.from_user.id}")
    else:
        await message.reply("История диалога уже пуста.")
        logger.info(f"Попытка очистки пустой истории для пользователя {message.from_user.id}")


@router.message()
async def text_handler(message: types.Message):
    """Обработчик всех текстовых сообщений через LLM."""
    if not message.text:
        return
    
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    await message.reply("Думаю...")
    logger.info(f"Пользователь {user_id} отправил сообщение: {message.text}")
    
    # Получаем историю диалога для данного чата
    history = chat_history.get(chat_id, [])
    
    # Отправляем запрос в LLM с историей
    answer = await llm_client.ask(message.text, history)
    
    if answer:
        # Добавляем вопрос и ответ в историю (без timestamp для совместимости с API)
        history.append({"role": "user", "content": message.text})
        history.append({"role": "assistant", "content": answer})
        
        # Сохраняем обновленную историю
        chat_history[chat_id] = history
        
        await message.reply(answer)
        logger.info(f"LLM ответ для пользователя {user_id}: {answer[:100]}...")
        logger.info(f"История диалога для чата {chat_id}: {len(history)} сообщений")
    else:
        await message.reply("Извините, произошла ошибка при обработке запроса.")
        logger.error(f"Ошибка получения ответа от LLM для пользователя {user_id}")
