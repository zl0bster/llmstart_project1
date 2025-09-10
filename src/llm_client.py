"""
Клиент для работы с LLM через OpenRouter API.
"""
import openai
import logging
import os
import hashlib
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
        self.history_max_turns = config['HISTORY_MAX_TURNS']
        
        # Загружаем системный промт из файла
        self.system_prompt = self._load_system_prompt()
        
        logger.info(f"LLM клиент инициализирован: модель {self.model}")
    
    def _load_system_prompt(self) -> str:
        """Загружает системный промт из файла."""
        prompt_path = os.getenv('SYSTEM_PROMPT_PATH', 'docs/system_prompt.md')
        
        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Логируем факт загрузки
            content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
            logger.info(f"Загружен системный промт из {prompt_path}, длина: {len(content)} символов, хеш: {content_hash}")
            
            return content
            
        except FileNotFoundError:
            logger.error(f"Файл системного промта не найден: {prompt_path}")
            return "Ты - полезный помощник."
        except Exception as e:
            logger.error(f"Ошибка загрузки системного промта: {e}")
            return "Ты - полезный помощник."
    
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
