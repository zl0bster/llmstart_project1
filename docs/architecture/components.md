# Детальное описание компонентов

## Обзор модулей

Система состоит из четырех основных модулей, каждый с четко определенной ответственностью.

## 1. src/bot.py — Точка входа

### Назначение
Главный модуль приложения, отвечающий за инициализацию и запуск бота.

### Основные функции

#### `setup_logging()`
```python
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
```

**Ответственность:**
- Создание директории для логов
- Настройка формата логирования
- Двойной вывод: в файл и консоль

#### `main()`
```python
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
```

**Ответственность:**
- Инициализация всех компонентов
- Создание экземпляра бота и диспетчера
- Регистрация обработчиков
- Запуск polling loop
- Обработка критических ошибок

## 2. src/handlers.py — Обработчики сообщений

### Назначение
Обработка входящих сообщений от пользователей Telegram и генерация ответов.

### Основные функции

#### `register_handlers(dp)`
```python
def register_handlers(dp: Dispatcher):
    """Регистрация всех обработчиков."""
    dp.message.register(start_command, Command("start"))
    dp.message.register(help_command, Command("help"))
    dp.message.register(reset_command, Command("reset"))
    dp.message.register(handle_text_message, F.text)
```

**Ответственность:**
- Регистрация обработчиков команд
- Регистрация обработчика текстовых сообщений
- Связывание функций с типами сообщений

#### `start_command(message: Message)`
```python
async def start_command(message: Message):
    """Обработчик команды /start."""
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    # Инициализация истории диалога
    if chat_id not in dialog_history:
        dialog_history[chat_id] = []
    
    # Генерация приветствия через LLM
    response = await generate_llm_response(
        "Привет! Я консультант компании ТехноСервис. Как дела?",
        chat_id
    )
    
    await message.answer(response)
```

**Ответственность:**
- Инициализация истории диалога для нового чата
- Генерация персонализированного приветствия
- Отправка ответа пользователю

#### `handle_text_message(message: Message)`
```python
async def handle_text_message(message: Message):
    """Обработчик текстовых сообщений."""
    chat_id = message.chat.id
    user_text = message.text
    
    # Логирование входящего сообщения
    logger.info(f"Получено сообщение от {message.from_user.id}: {user_text[:50]}...")
    
    # Генерация ответа через LLM
    response = await generate_llm_response(user_text, chat_id)
    
    # Отправка ответа
    await message.answer(response)
    
    # Логирование ответа
    logger.info(f"Отправлен ответ: {response[:50]}...")
```

**Ответственность:**
- Обработка всех текстовых сообщений
- Логирование входящих и исходящих сообщений
- Интеграция с LLM для генерации ответов
- Управление историей диалогов

### Управление историей диалогов

#### Глобальное хранилище
```python
# Глобальное хранилище истории диалогов
dialog_history: Dict[int, List[Dict]] = {}
```

**Структура истории:**
```python
{
    "role": "system|user|assistant",
    "content": "текст сообщения",
    "timestamp": datetime.now()
}
```

#### Функции управления
- **Добавление сообщения** — сохранение в историю
- **Ограничение размера** — `HISTORY_MAX_TURNS` последних реплик
- **Очистка истории** — команда `/reset`

## 3. src/llm_client.py — LLM интеграция

### Назначение
Адаптер для работы с OpenRouter API, обеспечивающий взаимодействие с языковыми моделями.

### Основные функции

#### `load_system_prompt()`
```python
def load_system_prompt() -> str:
    """Загрузка системного промта из файла."""
    config = get_config()
    prompt_path = config.get('SYSTEM_PROMPT_PATH', 'docs/system_prompt.md')
    
    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            prompt = f.read().strip()
        
        logger.info(f"Системный промт загружен из {prompt_path}, длина: {len(prompt)} символов")
        return prompt
        
    except FileNotFoundError:
        logger.error(f"Файл системного промта не найден: {prompt_path}")
        return "Ты полезный ИИ-помощник."
```

**Ответственность:**
- Загрузка системного промта из файла
- Обработка ошибок чтения файла
- Логирование процесса загрузки

#### `generate_response(messages: List[Dict], chat_id: int)`
```python
async def generate_response(messages: List[Dict], chat_id: int) -> str:
    """Генерация ответа через LLM."""
    config = get_config()
    
    try:
        # Создание клиента OpenAI для OpenRouter
        client = OpenAI(
            api_key=config['OPENROUTER_API_KEY'],
            base_url=config['OPENROUTER_API_URL']
        )
        
        # Подготовка сообщений для API
        api_messages = []
        for msg in messages:
            api_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Вызов API
        response = await client.chat.completions.create(
            model=config['LLM_MODEL_NAME'],
            messages=api_messages,
            temperature=config['LLM_TEMPERATURE'],
            max_tokens=config['LLM_MAX_TOKENS']
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"Ошибка при обращении к LLM: {e}")
        return "Извините, произошла ошибка при обработке вашего запроса."
```

**Ответственность:**
- Создание клиента для OpenRouter API
- Подготовка сообщений в формате API
- Вызов языковой модели
- Обработка ошибок API
- Возврат понятного сообщения об ошибке

### Обработка ошибок

#### Типы ошибок
1. **Сетевые ошибки** — таймауты, недоступность API
2. **Ошибки аутентификации** — неверный API ключ
3. **Ошибки лимитов** — превышение rate limits
4. **Ошибки модели** — недоступность модели

#### Стратегия обработки
- Логирование всех ошибок
- Возврат понятных сообщений пользователю
- Не прерывание работы бота при ошибках LLM

## 4. src/config.py — Управление конфигурацией

### Назначение
Централизованное управление всеми настройками приложения через переменные окружения.

### Основные функции

#### `get_config()`
```python
def get_config():
    """
    Получить конфигурацию приложения.
    
    Returns:
        dict: Словарь с настройками приложения
    """
    config = {
        'TELEGRAM_BOT_TOKEN': os.getenv('TELEGRAM_BOT_TOKEN'),
        'LOG_LEVEL': os.getenv('LOG_LEVEL', 'INFO'),
        'LOG_FILE': os.getenv('LOG_FILE', 'logs/bot.log'),
        # LLM настройки
        'OPENROUTER_API_KEY': os.getenv('OPENROUTER_API_KEY'),
        'OPENROUTER_API_URL': os.getenv('OPENROUTER_API_URL', 'https://openrouter.ai/api/v1'),
        'LLM_MODEL_NAME': os.getenv('LLM_MODEL_NAME', 'openai/gpt-3.5-turbo'),
        'LLM_TEMPERATURE': float(os.getenv('LLM_TEMPERATURE', '0.7')),
        'LLM_MAX_TOKENS': int(os.getenv('LLM_MAX_TOKENS', '500')),
        # История диалогов
        'SYSTEM_PROMPT': os.getenv('SYSTEM_PROMPT', 'Ты полезный ИИ-помощник. Отвечай кратко и по делу.'),
        'HISTORY_MAX_TURNS': int(os.getenv('HISTORY_MAX_TURNS', '5'))
    }
    
    # Валидация обязательных параметров
    if not config['TELEGRAM_BOT_TOKEN']:
        raise ValueError("TELEGRAM_BOT_TOKEN не найден в переменных окружения")
    
    if not config['OPENROUTER_API_KEY']:
        raise ValueError("OPENROUTER_API_KEY не найден в переменных окружения")
    
    return config
```

**Ответственность:**
- Загрузка всех переменных окружения
- Установка значений по умолчанию
- Валидация обязательных параметров
- Преобразование типов данных

### Структура конфигурации

#### Telegram настройки
- `TELEGRAM_BOT_TOKEN` — токен бота (обязательный)
- `LOG_LEVEL` — уровень логирования (по умолчанию: INFO)
- `LOG_FILE` — путь к файлу логов (по умолчанию: logs/bot.log)

#### LLM настройки
- `OPENROUTER_API_KEY` — ключ API (обязательный)
- `OPENROUTER_API_URL` — URL API (по умолчанию: OpenRouter)
- `LLM_MODEL_NAME` — модель (по умолчанию: gpt-3.5-turbo)
- `LLM_TEMPERATURE` — креативность (по умолчанию: 0.7)
- `LLM_MAX_TOKENS` — максимум токенов (по умолчанию: 500)

#### Настройки диалогов
- `SYSTEM_PROMPT` — системный промт (по умолчанию: базовый)
- `HISTORY_MAX_TURNS` — размер истории (по умолчанию: 5)

### Валидация конфигурации

#### Обязательные параметры
- `TELEGRAM_BOT_TOKEN` — без него бот не запустится
- `OPENROUTER_API_KEY` — без него LLM не работает

#### Проверка типов
- `LLM_TEMPERATURE` — преобразование в float
- `LLM_MAX_TOKENS` — преобразование в int
- `HISTORY_MAX_TURNS` — преобразование в int

## Взаимодействие компонентов

### Последовательность инициализации
1. **config.py** — загрузка конфигурации
2. **bot.py** — настройка логирования
3. **handlers.py** — регистрация обработчиков
4. **llm_client.py** — загрузка системного промта

### Поток обработки сообщения
1. **Telegram API** → **handlers.py** (получение сообщения)
2. **handlers.py** → **llm_client.py** (генерация ответа)
3. **llm_client.py** → **OpenRouter API** (запрос к LLM)
4. **llm_client.py** → **handlers.py** (возврат ответа)
5. **handlers.py** → **Telegram API** (отправка ответа)

### Управление состоянием
- **Глобальные переменные** — история диалогов
- **Конфигурация** — загружается один раз при старте
- **Логирование** — настраивается один раз при старте

---

**Следующий шаг:** [Быстрый старт](../setup/quick-start.md)
