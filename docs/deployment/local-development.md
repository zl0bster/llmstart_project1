# Локальная разработка

Руководство по разработке и отладке бота на локальной машине.

## Настройка среды разработки

### Требования
- **Python 3.11+** — основной язык
- **Git** — контроль версий
- **IDE/Editor** — VS Code, PyCharm, или любой другой
- **Terminal** — для выполнения команд

### Рекомендуемые инструменты

#### VS Code
```bash
# Установка расширений
code --install-extension ms-python.python
code --install-extension ms-python.pylint
code --install-extension ms-python.black-formatter
```

#### PyCharm
- Автоматическое определение виртуального окружения
- Встроенный отладчик
- Интеграция с Git

## Структура проекта

```
llmstart_project1-1/
├── src/                    # Исходный код
│   ├── bot.py             # Точка входа
│   ├── handlers.py        # Обработчики сообщений
│   ├── llm_client.py      # LLM интеграция
│   └── config.py          # Конфигурация
├── tests/                 # Тесты
├── docs/                  # Документация
├── logs/                  # Логи
├── data/                  # Данные
├── .env                   # Переменные окружения
├── requirements.txt       # Зависимости
├── Makefile              # Автоматизация
└── README.md             # Описание проекта
```

## Настройка виртуального окружения

### Создание окружения
```bash
# Создание виртуального окружения
python -m venv .venv

# Активация (Windows)
.venv\Scripts\activate

# Активация (Linux/Mac)
source .venv/bin/activate
```

### Установка зависимостей
```bash
# Обновление pip
python -m pip install --upgrade pip

# Установка зависимостей
pip install -r requirements.txt

# Или через Make
make install
```

### Проверка установки
```bash
# Проверка версий
python --version
pip list

# Проверка импортов
python -c "import aiogram; print('aiogram OK')"
python -c "import openai; print('openai OK')"
```

## Конфигурация для разработки

### .env для разработки
```env
# Telegram Bot Token
TELEGRAM_BOT_TOKEN=your_bot_token_here

# OpenRouter API Key
OPENROUTER_API_KEY=your_api_key_here

# Настройки для разработки
LOG_LEVEL=DEBUG
LOG_FILE=logs/bot.log
LLM_TEMPERATURE=0.9
LLM_MAX_TOKENS=1000
HISTORY_MAX_TURNS=10

# Системный промт
SYSTEM_PROMPT_PATH=docs/system_prompt.md
```

### Отладочные настройки
```env
# Дополнительные настройки для отладки
DEBUG_MODE=true
VERBOSE_LOGGING=true
MOCK_LLM=false
```

## Запуск в режиме разработки

### Базовый запуск
```bash
# Активация окружения
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Запуск бота
python src/bot.py
```

### Через Make
```bash
# Установка и запуск
make install
make run
```

### С отладкой
```bash
# Запуск с отладочными сообщениями
LOG_LEVEL=DEBUG python src/bot.py
```

## Отладка

### Логирование
```python
# В коде
import logging

logger = logging.getLogger(__name__)

# Отладочные сообщения
logger.debug("Отладочная информация")
logger.info("Информационное сообщение")
logger.warning("Предупреждение")
logger.error("Ошибка")
```

### Просмотр логов
```bash
# Просмотр логов в реальном времени
make logs

# Или напрямую
tail -f logs/bot.log

# Просмотр последних записей
tail -n 100 logs/bot.log
```

### Отладка в IDE

#### VS Code
1. Установите breakpoint
2. Нажмите F5 для запуска отладки
3. Выберите "Python File"

#### PyCharm
1. Установите breakpoint
2. Нажмите Shift+F9 для запуска отладки
3. Выберите конфигурацию

### Отладка асинхронного кода
```python
import asyncio
import logging

# Настройка логирования для asyncio
logging.basicConfig(level=logging.DEBUG)

async def debug_function():
    logger = logging.getLogger(__name__)
    logger.debug("Начало выполнения")
    
    # Ваш код здесь
    
    logger.debug("Завершение выполнения")

# Запуск с отладкой
asyncio.run(debug_function())
```

## Тестирование

### Запуск тестов
```bash
# Все тесты
make test

# Или напрямую
python -m pytest tests/

# С подробным выводом
python -m pytest tests/ -v

# Конкретный тест
python -m pytest tests/test_bot.py::test_function_name
```

### Структура тестов
```python
# tests/test_bot.py
import pytest
from src.config import get_config

def test_config_loading():
    """Тест загрузки конфигурации."""
    config = get_config()
    assert config['TELEGRAM_BOT_TOKEN'] is not None
    assert config['OPENROUTER_API_KEY'] is not None

def test_llm_client():
    """Тест LLM клиента."""
    # Тест логики здесь
    pass
```

### Мокирование внешних сервисов
```python
# tests/test_llm_client.py
import pytest
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
async def test_llm_response():
    """Тест ответа LLM с моком."""
    with patch('src.llm_client.OpenAI') as mock_openai:
        # Настройка мока
        mock_client = AsyncMock()
        mock_openai.return_value = mock_client
        
        # Тест логики
        result = await generate_response([], 12345)
        assert result is not None
```

## Hot Reload для разработки

### Установка watchdog
```bash
pip install watchdog
```

### Скрипт для hot reload
```python
# dev_server.py
import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class BotReloadHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print(f"Файл изменен: {event.src_path}")
            print("Перезапуск бота...")
            os.execv(sys.executable, [sys.executable] + sys.argv)

if __name__ == "__main__":
    event_handler = BotReloadHandler()
    observer = Observer()
    observer.schedule(event_handler, path='src/', recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
```

### Запуск с hot reload
```bash
# Запуск с автоматическим перезапуском
python dev_server.py
```

## Профилирование

### Измерение производительности
```python
import time
import cProfile
import pstats

def profile_function(func):
    """Декоратор для профилирования функций."""
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        
        result = func(*args, **kwargs)
        
        profiler.disable()
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        stats.print_stats(10)
        
        return result
    return wrapper

# Использование
@profile_function
async def generate_response(messages, chat_id):
    # Ваш код здесь
    pass
```

### Мониторинг памяти
```python
import psutil
import os

def monitor_memory():
    """Мониторинг использования памяти."""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    print(f"Использование памяти: {memory_info.rss / 1024 / 1024:.2f} MB")

# Вызов в коде
monitor_memory()
```

## Интеграция с IDE

### VS Code настройки
```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "./.venv/Scripts/python.exe",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests/"]
}
```

### PyCharm настройки
1. **File → Settings → Project → Python Interpreter**
2. Выберите интерпретатор из `.venv`
3. **Run → Edit Configurations**
4. Добавьте конфигурацию для `src/bot.py`

## Отладка проблем

### Частые проблемы разработки

#### "Module not found"
```bash
# Проверьте активацию окружения
which python
pip list

# Переустановите зависимости
pip install -r requirements.txt
```

#### "Import error"
```bash
# Проверьте PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Или запустите из корня проекта
python -m src.bot
```

#### "Permission denied"
```bash
# Проверьте права доступа
chmod +x .venv/Scripts/python.exe

# Или запустите через python
python src/bot.py
```

### Отладка асинхронного кода
```python
import asyncio
import logging

# Включение отладки asyncio
logging.basicConfig(level=logging.DEBUG)
asyncio.get_event_loop().set_debug(True)

# Запуск с отладкой
asyncio.run(main())
```

## Полезные команды

### Make команды
```bash
# Установка зависимостей
make install

# Запуск бота
make run

# Просмотр логов
make logs

# Запуск тестов
make test

# Очистка
make clean
```

### Прямые команды
```bash
# Активация окружения
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Запуск бота
python src/bot.py

# Просмотр логов
tail -f logs/bot.log

# Запуск тестов
python -m pytest tests/ -v
```

## Git workflow

### Настройка .gitignore
```gitignore
# Виртуальное окружение
.venv/
venv/

# Переменные окружения
.env
.env.*

# Логи
logs/*.log

# Кэш Python
__pycache__/
*.pyc
*.pyo

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

### Коммиты
```bash
# Добавление изменений
git add .

# Коммит с сообщением
git commit -m "feat: добавлена новая функция"

# Push в репозиторий
git push origin main
```

---

**Следующий шаг:** [Docker развертывание](docker-deployment.md)
