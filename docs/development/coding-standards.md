# Стандарты кодирования

Руководство по стилю кода и принципам разработки для проекта.

## Общие принципы

### KISS (Keep It Simple Stupid)
- **Простота** — выбирайте простое решение
- **Читаемость** — код должен быть понятен
- **Минимум абстракций** — не усложняйте без необходимости

### Итеративность
- **MVP подход** — начинайте с минимальной функциональности
- **Постепенное улучшение** — добавляйте функции по мере необходимости
- **Быстрые итерации** — возможность быстро вносить изменения

### Модульность
- **Единственная ответственность** — каждый модуль решает одну задачу
- **Слабая связанность** — модули не зависят друг от друга
- **Высокая когезия** — связанные функции в одном модуле

## Стиль кода

### PEP 8 и PEP 257
Следуйте стандартам Python:

```python
# Хорошо
def calculate_total_price(items: List[Item]) -> float:
    """Рассчитать общую стоимость товаров.
    
    Args:
        items: Список товаров
        
    Returns:
        Общая стоимость
    """
    return sum(item.price for item in items)

# Плохо
def calc(items):
    return sum(i.price for i in items)
```

### Именование

#### Переменные и функции
```python
# Хорошо - описательные имена
user_message = "Привет!"
dialog_history = []
max_tokens = 500

# Плохо - сокращения и аббревиатуры
msg = "Привет!"
hist = []
max_tok = 500
```

#### Константы
```python
# Хорошо - ВЕРХНИЙ_РЕГИСТР
DEFAULT_TEMPERATURE = 0.7
MAX_HISTORY_TURNS = 10
LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"

# Плохо
defaultTemperature = 0.7
maxHistoryTurns = 10
```

#### Классы
```python
# Хорошо - PascalCase
class LLMClient:
    pass

class TelegramBot:
    pass

# Плохо
class llm_client:
    pass

class telegramBot:
    pass
```

### Документирование

#### Docstrings
```python
def generate_response(messages: List[Dict], chat_id: int) -> str:
    """Генерация ответа через LLM.
    
    Args:
        messages: Список сообщений в формате OpenAI
        chat_id: ID чата для логирования
        
    Returns:
        Сгенерированный ответ
        
    Raises:
        OpenAIError: При ошибке API
        ValueError: При неверных параметрах
    """
    pass
```

#### Комментарии
```python
# Хорошо - объясняют "почему", а не "что"
# Ограничиваем историю для экономии токенов
if len(dialog_history) > MAX_HISTORY_TURNS:
    dialog_history = dialog_history[-MAX_HISTORY_TURNS:]

# Плохо - дублируют код
# Удаляем старые сообщения
dialog_history = dialog_history[-MAX_HISTORY_TURNS:]
```

### Типизация

#### Обязательная типизация
```python
from typing import List, Dict, Optional, Union

def process_message(
    message: str,
    user_id: int,
    chat_id: int
) -> Optional[str]:
    """Обработка сообщения пользователя."""
    pass

def get_config() -> Dict[str, Union[str, int, float]]:
    """Получить конфигурацию приложения."""
    pass
```

#### Типы для сложных структур
```python
from typing import TypedDict

class Message(TypedDict):
    role: str
    content: str
    timestamp: str

class DialogHistory(TypedDict):
    chat_id: int
    messages: List[Message]
```

## Структура кода

### Импорты
```python
# Стандартная библиотека
import os
import logging
from typing import List, Dict

# Сторонние библиотеки
import asyncio
from aiogram import Bot, Dispatcher
from openai import OpenAI

# Локальные модули
from src.config import get_config
from src.llm_client import generate_response
```

### Функции

#### Размер функций
```python
# Хорошо - короткие функции
def validate_token(token: str) -> bool:
    """Проверка валидности токена."""
    return token and len(token) > 10

def load_config() -> Dict:
    """Загрузка конфигурации."""
    config = {}
    # ... логика загрузки
    return config

# Плохо - длинная функция
def setup_bot():
    # 100+ строк кода
    pass
```

#### Параметры функций
```python
# Хорошо - не более 3-4 параметров
def send_message(bot: Bot, chat_id: int, text: str) -> None:
    pass

# Плохо - много параметров
def send_message(bot, chat_id, text, parse_mode, reply_to, keyboard, disable_notification, protect_content):
    pass
```

### Обработка ошибок

#### Try/except блоки
```python
# Хорошо - конкретные исключения
try:
    response = await client.chat.completions.create(...)
except openai.APITimeoutError:
    logger.error("Timeout при обращении к LLM")
    return "Извините, сервис временно недоступен"
except openai.RateLimitError:
    logger.error("Превышен лимит запросов")
    return "Слишком много запросов, попробуйте позже"
except Exception as e:
    logger.error(f"Неожиданная ошибка: {e}")
    return "Произошла ошибка, попробуйте позже"

# Плохо - общий except
try:
    response = await client.chat.completions.create(...)
except:
    return "Ошибка"
```

#### Fail-fast принцип
```python
# Хорошо - быстрая проверка
def process_message(message: str) -> str:
    if not message:
        raise ValueError("Сообщение не может быть пустым")
    
    if len(message) > 1000:
        raise ValueError("Сообщение слишком длинное")
    
    # Основная логика
    return process_text(message)
```

### Логирование

#### Уровни логирования
```python
import logging

logger = logging.getLogger(__name__)

# DEBUG - отладочная информация
logger.debug(f"Обработка сообщения: {message[:50]}...")

# INFO - основные события
logger.info(f"Получено сообщение от пользователя {user_id}")

# WARNING - предупреждения
logger.warning(f"Высокое использование токенов: {token_count}")

# ERROR - ошибки
logger.error(f"Ошибка при обращении к LLM: {e}")
```

#### Формат логов
```python
# Хорошо - структурированные логи
logger.info("LLM запрос", extra={
    "user_id": user_id,
    "message_length": len(message),
    "model": model_name
})

# Плохо - неструктурированные логи
logger.info(f"User {user_id} sent message of length {len(message)} to model {model_name}")
```

## Архитектурные принципы

### Разделение ответственности

#### Модули
```python
# src/config.py - только конфигурация
def get_config() -> Dict:
    """Загрузка конфигурации."""
    pass

# src/llm_client.py - только LLM
async def generate_response(messages: List[Dict]) -> str:
    """Генерация ответа через LLM."""
    pass

# src/handlers.py - только обработка сообщений
async def handle_message(message: Message) -> None:
    """Обработка сообщения."""
    pass
```

#### Функции
```python
# Хорошо - одна ответственность
def validate_config(config: Dict) -> bool:
    """Валидация конфигурации."""
    pass

def load_system_prompt() -> str:
    """Загрузка системного промта."""
    pass

# Плохо - несколько ответственностей
def setup_bot():
    # Валидация конфигурации
    # Загрузка промта
    # Создание бота
    # Регистрация обработчиков
    pass
```

### Зависимости

#### Импорты
```python
# Хорошо - явные зависимости
from src.config import get_config
from src.llm_client import generate_response

# Плохо - скрытые зависимости
import sys
sys.path.append('src')
from config import get_config
```

#### Инъекция зависимостей
```python
# Хорошо - зависимости передаются явно
class LLMClient:
    def __init__(self, api_key: str, base_url: str):
        self.client = OpenAI(api_key=api_key, base_url=base_url)

# Плохо - зависимости скрыты
class LLMClient:
    def __init__(self):
        config = get_config()  # Скрытая зависимость
        self.client = OpenAI(api_key=config['API_KEY'])
```

## Тестирование

### Структура тестов
```python
# tests/test_llm_client.py
import pytest
from unittest.mock import patch, AsyncMock
from src.llm_client import generate_response

class TestLLMClient:
    @pytest.mark.asyncio
    async def test_generate_response_success(self):
        """Тест успешной генерации ответа."""
        with patch('src.llm_client.OpenAI') as mock_openai:
            # Настройка мока
            mock_client = AsyncMock()
            mock_openai.return_value = mock_client
            
            # Тест
            result = await generate_response([], 12345)
            assert result is not None
    
    @pytest.mark.asyncio
    async def test_generate_response_error(self):
        """Тест обработки ошибки."""
        with patch('src.llm_client.OpenAI') as mock_openai:
            mock_client = AsyncMock()
            mock_client.chat.completions.create.side_effect = Exception("API Error")
            mock_openai.return_value = mock_client
            
            result = await generate_response([], 12345)
            assert "ошибка" in result.lower()
```

### Мокирование
```python
# Мокирование внешних сервисов
@patch('src.llm_client.OpenAI')
@patch('src.config.get_config')
async def test_llm_integration(mock_config, mock_openai):
    """Тест интеграции с LLM."""
    # Настройка моков
    mock_config.return_value = {
        'OPENROUTER_API_KEY': 'test-key',
        'LLM_MODEL_NAME': 'test-model'
    }
    
    # Тест логики
    pass
```

## Конфигурация

### Переменные окружения
```python
# Хорошо - явная загрузка
def get_config() -> Dict:
    config = {
        'TELEGRAM_BOT_TOKEN': os.getenv('TELEGRAM_BOT_TOKEN'),
        'LOG_LEVEL': os.getenv('LOG_LEVEL', 'INFO'),
    }
    
    # Валидация обязательных параметров
    if not config['TELEGRAM_BOT_TOKEN']:
        raise ValueError("TELEGRAM_BOT_TOKEN не найден")
    
    return config

# Плохо - глобальные переменные
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
```

### Значения по умолчанию
```python
# Хорошо - явные значения по умолчанию
def get_config() -> Dict:
    return {
        'LOG_LEVEL': os.getenv('LOG_LEVEL', 'INFO'),
        'LLM_TEMPERATURE': float(os.getenv('LLM_TEMPERATURE', '0.7')),
        'HISTORY_MAX_TURNS': int(os.getenv('HISTORY_MAX_TURNS', '5')),
    }

# Плохо - магические числа
def get_config() -> Dict:
    return {
        'LLM_TEMPERATURE': float(os.getenv('LLM_TEMPERATURE', '0.7')),  # Откуда 0.7?
        'HISTORY_MAX_TURNS': int(os.getenv('HISTORY_MAX_TURNS', '5')),  # Откуда 5?
    }
```

## Производительность

### Оптимизация
```python
# Хорошо - эффективные операции
def process_messages(messages: List[Dict]) -> List[Dict]:
    # Используем list comprehension
    return [msg for msg in messages if msg.get('role') == 'user']

# Плохо - неэффективные операции
def process_messages(messages: List[Dict]) -> List[Dict]:
    result = []
    for msg in messages:
        if msg.get('role') == 'user':
            result.append(msg)
    return result
```

### Кэширование
```python
# Хорошо - простое кэширование
from functools import lru_cache

@lru_cache(maxsize=128)
def load_system_prompt() -> str:
    """Загрузка системного промта с кэшированием."""
    with open('docs/system_prompt.md', 'r') as f:
        return f.read()
```

## Безопасность

### Валидация входных данных
```python
def validate_message(message: str) -> str:
    """Валидация сообщения пользователя."""
    if not message:
        raise ValueError("Сообщение не может быть пустым")
    
    if len(message) > 1000:
        raise ValueError("Сообщение слишком длинное")
    
    # Очистка от потенциально опасных символов
    return message.strip()
```

### Обработка секретов
```python
# Хорошо - секреты в переменных окружения
def get_config() -> Dict:
    return {
        'TELEGRAM_BOT_TOKEN': os.getenv('TELEGRAM_BOT_TOKEN'),
        'OPENROUTER_API_KEY': os.getenv('OPENROUTER_API_KEY'),
    }

# Плохо - секреты в коде
def get_config() -> Dict:
    return {
        'TELEGRAM_BOT_TOKEN': '1234567890:ABCdefGHIjklMNOpqrsTUVwxyz',
        'OPENROUTER_API_KEY': 'sk-or-v1-1234567890abcdef',
    }
```

## Инструменты

### Линтеры
```bash
# Установка
pip install flake8 black isort

# Проверка стиля
flake8 src/

# Форматирование
black src/
isort src/
```

### Pre-commit hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8
```

## Примеры кода

### Хороший код
```python
"""Модуль для работы с LLM клиентом."""

import logging
from typing import List, Dict
from openai import OpenAI

logger = logging.getLogger(__name__)

class LLMClient:
    """Клиент для работы с языковыми моделями."""
    
    def __init__(self, api_key: str, base_url: str, model: str):
        """Инициализация клиента.
        
        Args:
            api_key: API ключ OpenRouter
            base_url: URL API
            model: Название модели
        """
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
    
    async def generate_response(self, messages: List[Dict]) -> str:
        """Генерация ответа через LLM.
        
        Args:
            messages: Список сообщений
            
        Returns:
            Сгенерированный ответ
            
        Raises:
            OpenAIError: При ошибке API
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Ошибка при обращении к LLM: {e}")
            raise
```

### Плохой код
```python
import openai
import os

def get_response(msg):
    client = openai.OpenAI(api_key=os.getenv('API_KEY'))
    try:
        r = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': msg}]
        )
        return r.choices[0].message.content
    except:
        return 'error'
```

---

**Следующий шаг:** [Руководство по тестированию](testing.md)
