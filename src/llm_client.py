"""
Клиент для работы с LLM через OpenRouter API.
"""
import openai
import logging
from typing import Optional
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
        
        logger.info(f"LLM клиент инициализирован: модель {self.model}")
    
    async def ask(self, question: str) -> Optional[str]:
        """
        Отправить вопрос в LLM и получить ответ.
        
        Args:
            question: Текст вопроса пользователя
            
        Returns:
            Ответ от LLM или None в случае ошибки
        """
        try:
            logger.info(f"Отправка запроса в LLM: {question[:100]}...")
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": question}],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            answer = response.choices[0].message.content
            logger.info(f"Получен ответ от LLM: {answer[:100]}...")
            
            return answer
            
        except Exception as e:
            logger.error(f"Ошибка LLM API: {e}")
            return None
