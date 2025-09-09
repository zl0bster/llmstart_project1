"""
Клиент для работы с LLM через OpenRouter API.
"""
import openai
import logging
from typing import Optional, List, Dict
from config import get_config

logger = logging.getLogger(__name__)


class LLMClient:
    """Клиент для работы с LLM через OpenRouter API."""
    
    def __init__(self):
        """Инициализация клиента с настройками из конфигурации."""
        config = get_config()
        
        # Настройка для старой версии openai
        openai.api_key = config['OPENROUTER_API_KEY']
        openai.api_base = config['OPENROUTER_API_URL']
        
        self.model = config['LLM_MODEL_NAME']
        self.temperature = config['LLM_TEMPERATURE']
        self.max_tokens = config['LLM_MAX_TOKENS']
        self.system_prompt = config['SYSTEM_PROMPT']
        self.history_max_turns = config['HISTORY_MAX_TURNS']
        
        logger.info(f"LLM клиент инициализирован: модель {self.model}, системный промт: {self.system_prompt[:50]}...")
    
    async def ask(self, question: str, history: List[Dict] = None) -> Optional[str]:
        """
        Отправить вопрос в LLM и получить ответ.
        
        Args:
            question: Текст вопроса пользователя
            history: История диалога в формате [{"role": "user/assistant", "content": "текст"}]
            
        Returns:
            Ответ от LLM или None в случае ошибки
        """
        try:
            logger.info(f"Отправка запроса в LLM: {question[:100]}...")
            
            # Формируем сообщения с системным промтом и историей
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Добавляем последние N реплик из истории
            if history:
                recent_history = history[-self.history_max_turns:]
                messages.extend(recent_history)
                logger.info(f"Добавлена история диалога: {len(recent_history)} реплик")
            
            # Добавляем текущий вопрос
            messages.append({"role": "user", "content": question})
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            answer = response.choices[0].message.content
            logger.info(f"Получен ответ от LLM: {answer[:100]}...")
            
            return answer
            
        except Exception as e:
            logger.error(f"Ошибка LLM API: {e}")
            return None
