# Руководство по тестированию

Руководство по написанию и запуску тестов для Telegram-бота.

## Обзор тестирования

### Принципы тестирования
- **Покрытие** — тестируйте основную функциональность
- **Изоляция** — тесты не должны зависеть друг от друга
- **Детерминированность** — тесты должны давать одинаковый результат
- **Быстрота** — тесты должны выполняться быстро

### Типы тестов
- **Unit тесты** — тестирование отдельных функций
- **Integration тесты** — тестирование взаимодействия компонентов
- **Smoke тесты** — базовая проверка работоспособности

## Настройка тестов

### Установка pytest
```bash
# Установка pytest
pip install pytest pytest-asyncio pytest-mock

# Или через requirements.txt
echo "pytest==7.4.0" >> requirements.txt
echo "pytest-asyncio==0.21.0" >> requirements.txt
echo "pytest-mock==3.11.1" >> requirements.txt
```

### Структура тестов
```
tests/
├── __init__.py
├── test_bot.py              # Основные тесты
├── test_config.py           # Тесты конфигурации
├── test_llm_client.py       # Тесты LLM клиента
├── test_handlers.py         # Тесты обработчиков
└── conftest.py              # Конфигурация pytest
```

### Конфигурация pytest
```python
# conftest.py
import pytest
import asyncio
from unittest.mock import patch

@pytest.fixture
def event_loop():
    """Создание event loop для асинхронных тестов."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def mock_config():
    """Мок конфигурации для тестов."""
    return {
        'TELEGRAM_BOT_TOKEN': 'test_token',
        'OPENROUTER_API_KEY': 'test_api_key',
        'LLM_MODEL_NAME': 'test_model',
        'LLM_TEMPERATURE': 0.7,
        'LLM_MAX_TOKENS': 500,
        'HISTORY_MAX_TURNS': 5,
        'LOG_LEVEL': 'DEBUG',
        'LOG_FILE': 'test.log'
    }

@pytest.fixture
def mock_openai_client():
    """Мок OpenAI клиента."""
    with patch('src.llm_client.OpenAI') as mock:
        mock_client = mock.return_value
        mock_client.chat.completions.create = AsyncMock()
        yield mock_client
```

## Unit тесты

### Тестирование конфигурации
```python
# tests/test_config.py
import pytest
from unittest.mock import patch
from src.config import get_config

class TestConfig:
    def test_get_config_success(self, mock_config):
        """Тест успешной загрузки конфигурации."""
        with patch.dict('os.environ', {
            'TELEGRAM_BOT_TOKEN': 'test_token',
            'OPENROUTER_API_KEY': 'test_api_key'
        }):
            config = get_config()
            assert config['TELEGRAM_BOT_TOKEN'] == 'test_token'
            assert config['OPENROUTER_API_KEY'] == 'test_api_key'
    
    def test_get_config_missing_token(self):
        """Тест ошибки при отсутствии токена."""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="TELEGRAM_BOT_TOKEN не найден"):
                get_config()
    
    def test_get_config_default_values(self):
        """Тест значений по умолчанию."""
        with patch.dict('os.environ', {
            'TELEGRAM_BOT_TOKEN': 'test_token',
            'OPENROUTER_API_KEY': 'test_api_key'
        }):
            config = get_config()
            assert config['LOG_LEVEL'] == 'INFO'
            assert config['LLM_TEMPERATURE'] == 0.7
            assert config['HISTORY_MAX_TURNS'] == 5
```

### Тестирование LLM клиента
```python
# tests/test_llm_client.py
import pytest
from unittest.mock import patch, AsyncMock
from src.llm_client import generate_response, load_system_prompt

class TestLLMClient:
    @pytest.mark.asyncio
    async def test_generate_response_success(self, mock_openai_client):
        """Тест успешной генерации ответа."""
        # Настройка мока
        mock_openai_client.chat.completions.create.return_value = AsyncMock()
        mock_openai_client.chat.completions.create.return_value.choices = [
            AsyncMock()
        ]
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = "Test response"
        
        # Тест
        messages = [{"role": "user", "content": "Hello"}]
        result = await generate_response(messages, 12345)
        
        assert result == "Test response"
        mock_openai_client.chat.completions.create.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_generate_response_error(self, mock_openai_client):
        """Тест обработки ошибки API."""
        # Настройка мока для ошибки
        mock_openai_client.chat.completions.create.side_effect = Exception("API Error")
        
        # Тест
        messages = [{"role": "user", "content": "Hello"}]
        result = await generate_response(messages, 12345)
        
        assert "ошибка" in result.lower()
    
    def test_load_system_prompt_success(self):
        """Тест загрузки системного промта."""
        with patch('builtins.open', mock_open(read_data="Test prompt")):
            with patch('src.llm_client.get_config', return_value={'SYSTEM_PROMPT_PATH': 'test.md'}):
                result = load_system_prompt()
                assert result == "Test prompt"
    
    def test_load_system_prompt_file_not_found(self):
        """Тест обработки отсутствующего файла."""
        with patch('builtins.open', side_effect=FileNotFoundError):
            with patch('src.llm_client.get_config', return_value={'SYSTEM_PROMPT_PATH': 'missing.md'}):
                result = load_system_prompt()
                assert result == "Ты полезный ИИ-помощник."
```

### Тестирование обработчиков
```python
# tests/test_handlers.py
import pytest
from unittest.mock import patch, AsyncMock
from aiogram.types import Message, User, Chat
from src.handlers import start_command, handle_text_message

class TestHandlers:
    @pytest.mark.asyncio
    async def test_start_command(self):
        """Тест команды /start."""
        # Создание мока сообщения
        mock_message = AsyncMock(spec=Message)
        mock_message.from_user.id = 12345
        mock_message.chat.id = 67890
        mock_message.answer = AsyncMock()
        
        # Мок генерации ответа
        with patch('src.handlers.generate_llm_response', return_value="Привет!"):
            await start_command(mock_message)
            
            mock_message.answer.assert_called_once_with("Привет!")
    
    @pytest.mark.asyncio
    async def test_handle_text_message(self):
        """Тест обработки текстового сообщения."""
        # Создание мока сообщения
        mock_message = AsyncMock(spec=Message)
        mock_message.from_user.id = 12345
        mock_message.chat.id = 67890
        mock_message.text = "Hello"
        mock_message.answer = AsyncMock()
        
        # Мок генерации ответа
        with patch('src.handlers.generate_llm_response', return_value="Hi there!"):
            await handle_text_message(mock_message)
            
            mock_message.answer.assert_called_once_with("Hi there!")
```

## Integration тесты

### Тестирование полного потока
```python
# tests/test_integration.py
import pytest
from unittest.mock import patch, AsyncMock
from src.bot import main

class TestIntegration:
    @pytest.mark.asyncio
    async def test_bot_startup(self, mock_config):
        """Тест запуска бота."""
        with patch('src.config.get_config', return_value=mock_config):
            with patch('src.bot.setup_logging'):
                with patch('src.bot.Bot'):
                    with patch('src.bot.Dispatcher'):
                        with patch('src.bot.register_handlers'):
                            with patch('src.bot.dp.start_polling'):
                                # Тест должен пройти без ошибок
                                try:
                                    main()
                                except SystemExit:
                                    pass  # Ожидаемое поведение
    
    @pytest.mark.asyncio
    async def test_message_flow(self):
        """Тест полного потока обработки сообщения."""
        # Мок всех компонентов
        with patch('src.config.get_config') as mock_config:
            with patch('src.llm_client.generate_response') as mock_llm:
                with patch('src.handlers.dialog_history', {}):
                    # Настройка моков
                    mock_config.return_value = {
                        'TELEGRAM_BOT_TOKEN': 'test_token',
                        'OPENROUTER_API_KEY': 'test_api_key'
                    }
                    mock_llm.return_value = "Test response"
                    
                    # Тест потока
                    from src.handlers import handle_text_message
                    
                    mock_message = AsyncMock()
                    mock_message.text = "Hello"
                    mock_message.chat.id = 12345
                    mock_message.answer = AsyncMock()
                    
                    await handle_text_message(mock_message)
                    
                    # Проверки
                    mock_llm.assert_called_once()
                    mock_message.answer.assert_called_once_with("Test response")
```

## Smoke тесты

### Базовая проверка работоспособности
```python
# tests/test_smoke.py
import pytest
import sys
import os

class TestSmoke:
    def test_imports(self):
        """Тест импорта всех модулей."""
        try:
            import src.bot
            import src.config
            import src.handlers
            import src.llm_client
        except ImportError as e:
            pytest.fail(f"Ошибка импорта: {e}")
    
    def test_config_loading(self):
        """Тест загрузки конфигурации."""
        with patch.dict('os.environ', {
            'TELEGRAM_BOT_TOKEN': 'test_token',
            'OPENROUTER_API_KEY': 'test_api_key'
        }):
            from src.config import get_config
            config = get_config()
            assert config is not None
            assert isinstance(config, dict)
    
    def test_system_prompt_loading(self):
        """Тест загрузки системного промта."""
        with patch('builtins.open', mock_open(read_data="Test prompt")):
            with patch('src.llm_client.get_config', return_value={'SYSTEM_PROMPT_PATH': 'test.md'}):
                from src.llm_client import load_system_prompt
                prompt = load_system_prompt()
                assert prompt is not None
                assert isinstance(prompt, str)
```

## Мокирование

### Мокирование внешних сервисов
```python
# tests/test_mocks.py
import pytest
from unittest.mock import patch, AsyncMock, MagicMock

class TestMocks:
    @pytest.mark.asyncio
    async def test_telegram_api_mock(self):
        """Тест мокирования Telegram API."""
        with patch('aiogram.Bot') as mock_bot:
            mock_bot_instance = AsyncMock()
            mock_bot.return_value = mock_bot_instance
            
            # Тест логики с моком
            bot = mock_bot(token="test_token")
            await bot.get_me()
            
            mock_bot_instance.get_me.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_openai_api_mock(self):
        """Тест мокирования OpenAI API."""
        with patch('openai.OpenAI') as mock_openai:
            mock_client = AsyncMock()
            mock_openai.return_value = mock_client
            
            # Настройка ответа
            mock_response = AsyncMock()
            mock_response.choices = [AsyncMock()]
            mock_response.choices[0].message.content = "Test response"
            mock_client.chat.completions.create.return_value = mock_response
            
            # Тест
            client = mock_openai(api_key="test_key")
            response = await client.chat.completions.create(
                model="test-model",
                messages=[{"role": "user", "content": "Hello"}]
            )
            
            assert response.choices[0].message.content == "Test response"
```

### Мокирование файловой системы
```python
# tests/test_file_mocks.py
import pytest
from unittest.mock import patch, mock_open

class TestFileMocks:
    def test_config_file_reading(self):
        """Тест чтения конфигурационного файла."""
        config_content = """
        TELEGRAM_BOT_TOKEN=test_token
        OPENROUTER_API_KEY=test_api_key
        """
        
        with patch('builtins.open', mock_open(read_data=config_content)):
            with patch('os.path.exists', return_value=True):
                # Тест логики чтения файла
                pass
    
    def test_system_prompt_file_reading(self):
        """Тест чтения файла системного промта."""
        prompt_content = "Ты полезный ИИ-помощник."
        
        with patch('builtins.open', mock_open(read_data=prompt_content)):
            with patch('src.llm_client.get_config', return_value={'SYSTEM_PROMPT_PATH': 'test.md'}):
                from src.llm_client import load_system_prompt
                result = load_system_prompt()
                assert result == prompt_content
```

## Запуск тестов

### Базовый запуск
```bash
# Все тесты
pytest

# С подробным выводом
pytest -v

# Конкретный файл
pytest tests/test_config.py

# Конкретный тест
pytest tests/test_config.py::TestConfig::test_get_config_success
```

### Запуск с покрытием
```bash
# Установка coverage
pip install pytest-cov

# Запуск с покрытием
pytest --cov=src --cov-report=html

# Просмотр отчета
open htmlcov/index.html
```

### Запуск через Make
```bash
# Запуск тестов
make test

# Запуск с покрытием
make test-coverage
```

### Конфигурация Makefile
```makefile
# Makefile
test:
	.venv\Scripts\activate && python -m pytest tests/ -v

test-coverage:
	.venv\Scripts\activate && python -m pytest tests/ --cov=src --cov-report=html

test-fast:
	.venv\Scripts\activate && python -m pytest tests/ -v --tb=short
```

## CI/CD интеграция

### GitHub Actions
```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          pytest tests/ -v --cov=src --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v1
        with:
          file: ./coverage.xml
```

## Лучшие практики

### Написание тестов
```python
# Хорошо - описательные имена
def test_generate_response_returns_string_when_api_success():
    """Тест возврата строки при успешном API."""
    pass

# Плохо - неописательные имена
def test_1():
    pass

def test_response():
    pass
```

### Структура тестов
```python
# Хорошо - AAA паттерн
def test_function():
    # Arrange - подготовка
    input_data = "test input"
    expected_output = "test output"
    
    # Act - выполнение
    result = function_under_test(input_data)
    
    # Assert - проверка
    assert result == expected_output
```

### Изоляция тестов
```python
# Хорошо - каждый тест независим
def test_function_1():
    # Тест не зависит от других тестов
    pass

def test_function_2():
    # Тест не зависит от других тестов
    pass

# Плохо - тесты зависят друг от друга
def test_function_1():
    global_state = "modified"

def test_function_2():
    assert global_state == "modified"  # Зависит от предыдущего теста
```

## Troubleshooting

### Частые проблемы

#### "Module not found"
```bash
# Проверьте PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Или запустите из корня проекта
python -m pytest tests/
```

#### "Async test not running"
```bash
# Убедитесь, что установлен pytest-asyncio
pip install pytest-asyncio

# Используйте @pytest.mark.asyncio
@pytest.mark.asyncio
async def test_async_function():
    pass
```

#### "Mock not working"
```bash
# Проверьте путь к моку
with patch('src.module.function') as mock:
    pass

# Убедитесь, что мок применяется до импорта
```

---

**Следующий шаг:** [Мониторинг и логирование](../operations/monitoring.md)
