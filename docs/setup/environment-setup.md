# Детальная настройка окружения

Полное руководство по настройке всех компонентов системы.

## Структура конфигурации

### Файл .env
Все настройки приложения хранятся в файле `.env` в корне проекта.

```env
# ===========================================
# TELEGRAM BOT НАСТРОЙКИ
# ===========================================

# Токен бота (обязательный)
# Получить: https://t.me/BotFather
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# ===========================================
# ЛОГИРОВАНИЕ
# ===========================================

# Уровень логирования: DEBUG, INFO, WARNING, ERROR
LOG_LEVEL=INFO

# Путь к файлу логов
LOG_FILE=logs/bot.log

# ===========================================
# LLM НАСТРОЙКИ (OpenRouter)
# ===========================================

# API ключ OpenRouter (обязательный)
# Получить: https://openrouter.ai/keys
OPENROUTER_API_KEY=sk-or-v1-your-api-key-here

# URL API (обычно не нужно менять)
OPENROUTER_API_URL=https://openrouter.ai/api/v1

# Модель LLM
LLM_MODEL_NAME=openai/gpt-3.5-turbo

# Креативность ответов (0.0 - 2.0)
LLM_TEMPERATURE=0.7

# Максимальное количество токенов в ответе
LLM_MAX_TOKENS=500

# ===========================================
# ДИАЛОГИ И КОНТЕКСТ
# ===========================================

# Системный промт (по умолчанию из файла)
SYSTEM_PROMPT=Ты полезный ИИ-помощник. Отвечай кратко и по делу.

# Максимальное количество реплик в истории
HISTORY_MAX_TURNS=5

# Путь к файлу системного промта
SYSTEM_PROMPT_PATH=docs/system_prompt.md
```

## Детальная настройка параметров

### Telegram Bot настройки

#### TELEGRAM_BOT_TOKEN
**Обязательный параметр**

Получение токена:
1. Найдите [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте `/newbot`
3. Введите имя бота (например: "Мой Консультант")
4. Введите username (должен заканчиваться на `bot`)
5. Скопируйте полученный токен

**Пример:**
```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

**Проверка:**
```bash
# Проверка токена через API
curl "https://api.telegram.org/bot<YOUR_TOKEN>/getMe"
```

### LLM настройки (OpenRouter)

#### OPENROUTER_API_KEY
**Обязательный параметр**

Получение ключа:
1. Зарегистрируйтесь на [OpenRouter](https://openrouter.ai/)
2. Перейдите в раздел "Keys"
3. Нажмите "Create Key"
4. Скопируйте ключ (начинается с `sk-or-v1-`)

**Пример:**
```env
OPENROUTER_API_KEY=sk-or-v1-1234567890abcdef1234567890abcdef
```

#### LLM_MODEL_NAME
**Рекомендуемые модели:**

| Модель | Описание | Стоимость | Скорость |
|--------|----------|-----------|----------|
| `openai/gpt-3.5-turbo` | Быстрая, дешевая | $0.0015/1K токенов | Быстрая |
| `openai/gpt-4` | Качественная | $0.03/1K токенов | Медленная |
| `anthropic/claude-3-haiku` | Быстрая, качественная | $0.00025/1K токенов | Быстрая |
| `google/gemini-pro` | Хорошее качество | $0.0005/1K токенов | Средняя |

**Пример:**
```env
LLM_MODEL_NAME=openai/gpt-3.5-turbo
```

#### LLM_TEMPERATURE
**Влияет на креативность ответов:**

- `0.0` — детерминированные, предсказуемые ответы
- `0.7` — сбалансированные ответы (по умолчанию)
- `1.0` — креативные, разнообразные ответы
- `2.0` — очень креативные, иногда странные ответы

**Рекомендации:**
- Для консультаций: `0.3-0.7`
- Для творческих задач: `0.8-1.2`

#### LLM_MAX_TOKENS
**Максимальная длина ответа:**

- `100` — очень короткие ответы
- `500` — средние ответы (по умолчанию)
- `1000` — длинные ответы
- `2000` — очень длинные ответы

**Рекомендации:**
- Для быстрых ответов: `200-500`
- Для подробных консультаций: `800-1500`

### Настройки логирования

#### LOG_LEVEL
**Уровни логирования:**

- `DEBUG` — все события (для разработки)
- `INFO` — основные события (по умолчанию)
- `WARNING` — предупреждения
- `ERROR` — только ошибки

**Пример:**
```env
LOG_LEVEL=INFO
```

#### LOG_FILE
**Путь к файлу логов:**

```env
LOG_FILE=logs/bot.log
```

**Создание директории:**
```bash
mkdir -p logs
```

### Настройки диалогов

#### HISTORY_MAX_TURNS
**Размер истории диалога:**

- `3` — короткая память
- `5` — средняя память (по умолчанию)
- `10` — длинная память
- `20` — очень длинная память

**Влияние на производительность:**
- Больше реплик = больше токенов = выше стоимость
- Рекомендуется: `5-10` для большинства случаев

#### SYSTEM_PROMPT_PATH
**Путь к файлу системного промта:**

```env
SYSTEM_PROMPT_PATH=docs/system_prompt.md
```

## Настройка виртуального окружения

### Создание окружения
```bash
# Python 3.11+
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

# Установка из requirements.txt
pip install -r requirements.txt

# Или установка по отдельности
pip install aiogram==3.0.0
pip install openai==1.0.0
pip install python-dotenv==1.0.0
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

## Настройка системного промта

### Редактирование промта
Откройте файл `docs/system_prompt.md` и отредактируйте под ваши нужды:

```markdown
# Системный промт для бота-консультанта

Ты - профессиональный консультант компании "Ваша Компания". 

## Твоя роль:
- Дружелюбный и профессиональный помощник
- Эксперт по услугам компании
- Помощник в решении проблем клиентов

## О компании:
Мы предоставляем следующие услуги:
- Услуга 1
- Услуга 2
- Услуга 3

## Стиль общения:
- Вежливый и профессиональный тон
- Понятный язык без сложных терминов
- Конкретные предложения решений
```

### Загрузка промта из файла
Система автоматически загружает промт из файла при запуске:

```python
# В src/llm_client.py
def load_system_prompt() -> str:
    config = get_config()
    prompt_path = config.get('SYSTEM_PROMPT_PATH', 'docs/system_prompt.md')
    
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read().strip()
```

## Проверка конфигурации

### Тест конфигурации
```bash
# Проверка загрузки конфигурации
python -c "from src.config import get_config; print('Config OK:', get_config()['TELEGRAM_BOT_TOKEN'][:10] + '...')"
```

### Тест Telegram API
```bash
# Проверка токена бота
python -c "
import asyncio
from aiogram import Bot
from src.config import get_config

async def test_bot():
    config = get_config()
    bot = Bot(token=config['TELEGRAM_BOT_TOKEN'])
    me = await bot.get_me()
    print(f'Bot OK: @{me.username}')
    await bot.session.close()

asyncio.run(test_bot())
"
```

### Тест OpenRouter API
```bash
# Проверка API ключа
python -c "
from openai import OpenAI
from src.config import get_config

config = get_config()
client = OpenAI(
    api_key=config['OPENROUTER_API_KEY'],
    base_url=config['OPENROUTER_API_URL']
)

response = client.chat.completions.create(
    model=config['LLM_MODEL_NAME'],
    messages=[{'role': 'user', 'content': 'Привет!'}],
    max_tokens=10
)

print('OpenRouter OK:', response.choices[0].message.content)
"
```

## Переменные окружения для разных сред

### Разработка (.env.development)
```env
LOG_LEVEL=DEBUG
LLM_TEMPERATURE=0.9
LLM_MAX_TOKENS=1000
HISTORY_MAX_TURNS=10
```

### Продакшн (.env.production)
```env
LOG_LEVEL=INFO
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=500
HISTORY_MAX_TURNS=5
```

### Тестирование (.env.testing)
```env
LOG_LEVEL=ERROR
LLM_TEMPERATURE=0.0
LLM_MAX_TOKENS=100
HISTORY_MAX_TURNS=3
```

## Безопасность

### Защита секретов
```bash
# Добавьте .env в .gitignore
echo ".env" >> .gitignore
echo ".env.*" >> .gitignore

# Проверьте, что .env не в git
git status
```

### Ротация ключей
- Регулярно обновляйте API ключи
- Используйте разные ключи для разных сред
- Мониторьте использование API

### Ограничения доступа
```bash
# Ограничьте права доступа к .env
chmod 600 .env
```

## Troubleshooting

### Частые ошибки

#### "TELEGRAM_BOT_TOKEN не найден"
```bash
# Проверьте файл .env
cat .env | grep TELEGRAM_BOT_TOKEN

# Проверьте, что файл существует
ls -la .env
```

#### "OpenRouter API недоступен"
```bash
# Проверьте ключ
cat .env | grep OPENROUTER_API_KEY

# Проверьте интернет
ping openrouter.ai
```

#### "Модуль не найден"
```bash
# Проверьте виртуальное окружение
which python
pip list

# Переустановите зависимости
pip install -r requirements.txt
```

---

**Следующий шаг:** [Настройка LLM интеграции](llm-integration.md)
