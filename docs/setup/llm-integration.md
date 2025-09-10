# Настройка интеграции с LLM

Руководство по настройке и оптимизации работы с языковыми моделями через OpenRouter.

## Обзор OpenRouter

OpenRouter — это агрегатор языковых моделей, предоставляющий единый API для доступа к различным LLM.

### Преимущества
- **Единый API** — один интерфейс для всех моделей
- **Прозрачные цены** — четкое ценообразование
- **Быстрый доступ** — без ожидания в очереди
- **Множество моделей** — от GPT до Claude и Gemini

## Настройка аккаунта

### Регистрация
1. Перейдите на [OpenRouter](https://openrouter.ai/)
2. Нажмите "Sign Up"
3. Подтвердите email
4. Заполните профиль

### Получение API ключа
1. Войдите в аккаунт
2. Перейдите в раздел "Keys"
3. Нажмите "Create Key"
4. Введите название ключа (например: "Telegram Bot")
5. Скопируйте ключ (начинается с `sk-or-v1-`)

### Настройка в .env
```env
OPENROUTER_API_KEY=sk-or-v1-1234567890abcdef1234567890abcdef
OPENROUTER_API_URL=https://openrouter.ai/api/v1
```

## Выбор модели

### Рекомендуемые модели

#### Для быстрых ответов
| Модель | Скорость | Качество | Стоимость |
|--------|----------|----------|-----------|
| `openai/gpt-3.5-turbo` | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | $0.0015/1K |
| `anthropic/claude-3-haiku` | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | $0.00025/1K |
| `google/gemini-pro` | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | $0.0005/1K |

#### Для качественных ответов
| Модель | Скорость | Качество | Стоимость |
|--------|----------|----------|-----------|
| `openai/gpt-4` | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | $0.03/1K |
| `anthropic/claude-3-sonnet` | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | $0.003/1K |
| `google/gemini-pro` | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | $0.0005/1K |

#### Для креативных задач
| Модель | Креативность | Качество | Стоимость |
|--------|--------------|----------|-----------|
| `openai/gpt-4` | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | $0.03/1K |
| `anthropic/claude-3-sonnet` | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | $0.003/1K |
| `meta-llama/llama-2-70b-chat` | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | $0.0007/1K |

### Настройка модели в .env
```env
# Для быстрых ответов
LLM_MODEL_NAME=openai/gpt-3.5-turbo

# Для качественных ответов
LLM_MODEL_NAME=anthropic/claude-3-sonnet

# Для креативных задач
LLM_MODEL_NAME=openai/gpt-4
```

## Оптимизация параметров

### Temperature (Креативность)

#### Настройка для разных задач

**Консультации (0.3-0.7):**
```env
LLM_TEMPERATURE=0.5
```

**Творческие задачи (0.8-1.2):**
```env
LLM_TEMPERATURE=1.0
```

**Детерминированные ответы (0.0-0.3):**
```env
LLM_TEMPERATURE=0.1
```

#### Влияние на ответы
- `0.0` — всегда одинаковые ответы
- `0.5` — сбалансированные ответы
- `1.0` — разнообразные ответы
- `2.0` — очень креативные ответы

### Max Tokens (Длина ответа)

#### Рекомендации по длине

**Короткие ответы (100-300 токенов):**
```env
LLM_MAX_TOKENS=200
```

**Средние ответы (300-800 токенов):**
```env
LLM_MAX_TOKENS=500
```

**Длинные ответы (800-2000 токенов):**
```env
LLM_MAX_TOKENS=1500
```

#### Соотношение токенов и символов
- 1 токен ≈ 0.75 слова (английский)
- 1 токен ≈ 0.5 слова (русский)
- 100 токенов ≈ 75 слов ≈ 375 символов

### История диалогов

#### Настройка контекста
```env
# Короткая память (быстро, дешево)
HISTORY_MAX_TURNS=3

# Средняя память (сбалансированно)
HISTORY_MAX_TURNS=5

# Длинная память (качественно, дорого)
HISTORY_MAX_TURNS=10
```

#### Влияние на стоимость
- Больше реплик = больше токенов = выше стоимость
- Рекомендуется: 5-7 реплик для большинства случаев

## Системный промт

### Структура промта
```markdown
# Системный промт для бота-консультанта

Ты - профессиональный консультант компании "ТехноСервис". 

## Твоя роль:
- Дружелюбный и профессиональный помощник
- Эксперт по услугам компании
- Помощник в решении проблем клиентов

## О компании:
Мы предоставляем IT-услуги для бизнеса:
- Разработка веб-сайтов и мобильных приложений
- Настройка и поддержка IT-инфраструктуры
- Консультации по цифровой трансформации

## Стиль общения:
- Вежливый и профессиональный тон
- Понятный язык без сложных терминов
- Конкретные предложения решений
```

### Оптимизация промта

#### Принципы написания
1. **Четкость** — конкретные инструкции
2. **Контекст** — информация о компании
3. **Ограничения** — что можно и нельзя
4. **Примеры** — образцы ответов

#### Длина промта
- **Короткий** (100-300 токенов) — базовые инструкции
- **Средний** (300-800 токенов) — детальные инструкции
- **Длинный** (800+ токенов) — полная информация

### Загрузка из файла
```env
SYSTEM_PROMPT_PATH=docs/system_prompt.md
```

## Мониторинг использования

### Отслеживание токенов
```python
# В src/llm_client.py
async def generate_response(messages, chat_id):
    # ... код генерации ...
    
    # Логирование использования
    logger.info(f"LLM запрос: {len(messages)} сообщений, "
                f"ответ: {len(response)} символов")
    
    return response
```

### Контроль расходов
1. **Установите лимиты** в OpenRouter
2. **Мониторьте логи** на предмет больших запросов
3. **Оптимизируйте промт** для уменьшения токенов
4. **Используйте кэширование** для повторных запросов

## Обработка ошибок

### Типы ошибок OpenRouter

#### Rate Limit (429)
```python
# Обработка превышения лимитов
if response.status_code == 429:
    retry_after = response.headers.get('Retry-After', 60)
    await asyncio.sleep(retry_after)
    return await generate_response(messages, chat_id)
```

#### Недоступность модели (503)
```python
# Fallback на другую модель
if response.status_code == 503:
    config['LLM_MODEL_NAME'] = 'openai/gpt-3.5-turbo'
    return await generate_response(messages, chat_id)
```

#### Неверный API ключ (401)
```python
# Проверка ключа
if response.status_code == 401:
    logger.error("Неверный OpenRouter API ключ")
    return "Извините, произошла ошибка конфигурации."
```

### Стратегия retry
```python
import asyncio
from functools import wraps

def retry_on_error(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    await asyncio.sleep(delay * (2 ** attempt))
            return None
        return wrapper
    return decorator

@retry_on_error(max_retries=3, delay=1)
async def generate_response(messages, chat_id):
    # ... код генерации ...
```

## Тестирование интеграции

### Проверка подключения
```bash
# Тест API ключа
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

### Тест системного промта
```bash
# Тест загрузки промта
python -c "
from src.llm_client import load_system_prompt
prompt = load_system_prompt()
print('Промт загружен, длина:', len(prompt))
print('Первые 100 символов:', prompt[:100])
"
```

### Тест полной интеграции
```bash
# Тест генерации ответа
python -c "
import asyncio
from src.llm_client import generate_llm_response

async def test():
    response = await generate_llm_response('Привет!', 12345)
    print('Ответ:', response)

asyncio.run(test())
"
```

## Оптимизация производительности

### Кэширование ответов
```python
# Простое кэширование в памяти
response_cache = {}

async def generate_response_cached(messages, chat_id):
    # Создаем ключ кэша
    cache_key = hash(str(messages))
    
    # Проверяем кэш
    if cache_key in response_cache:
        return response_cache[cache_key]
    
    # Генерируем ответ
    response = await generate_response(messages, chat_id)
    
    # Сохраняем в кэш
    response_cache[cache_key] = response
    
    return response
```

### Асинхронная обработка
```python
# Обработка нескольких запросов параллельно
async def process_multiple_requests(requests):
    tasks = [generate_response(msg, chat_id) for msg, chat_id in requests]
    responses = await asyncio.gather(*tasks, return_exceptions=True)
    return responses
```

### Оптимизация промта
```python
# Сжатие промта для экономии токенов
def compress_prompt(prompt):
    # Удаление лишних пробелов
    prompt = ' '.join(prompt.split())
    
    # Удаление повторяющихся фраз
    # ... логика сжатия ...
    
    return prompt
```

## Troubleshooting

### Частые проблемы

#### "Model not found"
- Проверьте название модели в `.env`
- Убедитесь, что модель доступна в OpenRouter
- Попробуйте другую модель

#### "Rate limit exceeded"
- Уменьшите частоту запросов
- Увеличьте задержки между запросами
- Рассмотрите upgrade плана

#### "Invalid API key"
- Проверьте ключ в `.env`
- Убедитесь, что ключ активен
- Создайте новый ключ

#### "Context length exceeded"
- Уменьшите `HISTORY_MAX_TURNS`
- Сократите системный промт
- Уменьшите `LLM_MAX_TOKENS`

### Диагностика
```bash
# Проверка статуса OpenRouter
curl -H "Authorization: Bearer $OPENROUTER_API_KEY" \
     https://openrouter.ai/api/v1/models

# Проверка баланса
curl -H "Authorization: Bearer $OPENROUTER_API_KEY" \
     https://openrouter.ai/api/v1/auth/key
```

---

**Следующий шаг:** [Локальная разработка](../deployment/local-development.md)
