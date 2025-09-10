# Развертывание на Railway.com

Руководство по развертыванию Telegram-бота на платформе Railway.com из Git репозитория.

## Обзор Railway.com

Railway.com — это современная платформа для развертывания приложений с автоматическим CI/CD из Git репозиториев.

### Преимущества Railway.com
- **Автоматическое развертывание** — из Git репозитория
- **Простота настройки** — минимум конфигурации
- **Встроенные переменные окружения** — безопасное хранение секретов
- **Автомасштабирование** — по требованию
- **Мониторинг** — встроенные метрики и логи

## Подготовка проекта

### 1. Исправление Dockerfile

**Проблема:** Текущий Dockerfile содержит строку `COPY .env .`, которая вызывает ошибку при развертывании, так как файл `.env` не включен в Git репозиторий.

**Решение:** Удалить строку копирования `.env` файла из Dockerfile.

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Копирование зависимостей и установка
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY src/ ./src/

# Создание директорий для логов и данных
RUN mkdir -p logs data

# Точка входа
CMD ["python", "src/bot.py"]
```

### 2. Проверка .gitignore

Убедитесь, что файл `.env` исключен из Git:

```gitignore
# Переменные окружения
.env
.env.local
.env.*.local
```

### 3. Подготовка переменных окружения

Создайте список всех необходимых переменных из `env.example`:

```env
# Обязательные переменные
TELEGRAM_BOT_TOKEN=your_bot_token_here
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Настройки логирования
LOG_LEVEL=INFO
LOG_FILE=logs/bot.log

# LLM настройки
OPENROUTER_API_URL=https://openrouter.ai/api/v1
LLM_MODEL_NAME=openai/gpt-3.5-turbo
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=200

# История диалогов
SYSTEM_PROMPT=Ты полезный ИИ-помощник. Отвечай кратко и по делу.
HISTORY_MAX_TURNS=5

# Системный промт из файла
SYSTEM_PROMPT_PATH=docs/system_prompt.md
```

## Пошаговое развертывание

### Шаг 1: Регистрация на Railway.com

1. Перейдите на [railway.com](https://railway.com)
2. Нажмите **"Start a New Project"**
3. Войдите через GitHub (рекомендуется)

### Шаг 2: Подключение репозитория

1. Выберите **"Deploy from GitHub repo"**
2. Найдите и выберите ваш репозиторий `llmstart_project1-1`
3. Нажмите **"Deploy Now"**

### Шаг 3: Настройка переменных окружения

#### 3.1. Открытие настроек переменных

1. В панели Railway.com выберите ваш проект
2. Перейдите на вкладку **"Variables"**
3. Нажмите **"New Variable"**

#### 3.2. Добавление обязательных переменных

Добавьте каждую переменную по отдельности:

**Telegram Bot Token:**
- **Name:** `TELEGRAM_BOT_TOKEN`
- **Value:** `ваш_токен_от_botfather`
- **Type:** `Secret` (рекомендуется)

**OpenRouter API Key:**
- **Name:** `OPENROUTER_API_KEY`
- **Value:** `ваш_api_ключ_от_openrouter`
- **Type:** `Secret` (обязательно)

**Настройки логирования:**
- **Name:** `LOG_LEVEL`
- **Value:** `INFO`
- **Type:** `Plain`

- **Name:** `LOG_FILE`
- **Value:** `logs/bot.log`
- **Type:** `Plain`

**LLM настройки:**
- **Name:** `OPENROUTER_API_URL`
- **Value:** `https://openrouter.ai/api/v1`
- **Type:** `Plain`

- **Name:** `LLM_MODEL_NAME`
- **Value:** `openai/gpt-3.5-turbo`
- **Type:** `Plain`

- **Name:** `LLM_TEMPERATURE`
- **Value:** `0.7`
- **Type:** `Plain`

- **Name:** `LLM_MAX_TOKENS`
- **Value:** `200`
- **Type:** `Plain`

**История диалогов:**
- **Name:** `SYSTEM_PROMPT`
- **Value:** `Ты полезный ИИ-помощник. Отвечай кратко и по делу.`
- **Type:** `Plain`

- **Name:** `HISTORY_MAX_TURNS`
- **Value:** `5`
- **Type:** `Plain`

**Системный промт:**
- **Name:** `SYSTEM_PROMPT_PATH`
- **Value:** `docs/system_prompt.md`
- **Type:** `Plain`

#### 3.3. Массовое добавление переменных

Альтернативно, можно добавить все переменные сразу:

1. Нажмите **"Raw Editor"** в разделе Variables
2. Вставьте JSON с переменными:

```json
{
  "TELEGRAM_BOT_TOKEN": "ваш_токен_от_botfather",
  "OPENROUTER_API_KEY": "ваш_api_ключ_от_openrouter",
  "LOG_LEVEL": "INFO",
  "LOG_FILE": "logs/bot.log",
  "OPENROUTER_API_URL": "https://openrouter.ai/api/v1",
  "LLM_MODEL_NAME": "openai/gpt-3.5-turbo",
  "LLM_TEMPERATURE": "0.7",
  "LLM_MAX_TOKENS": "200",
  "SYSTEM_PROMPT": "Ты полезный ИИ-помощник. Отвечай кратко и по делу.",
  "HISTORY_MAX_TURNS": "5",
  "SYSTEM_PROMPT_PATH": "docs/system_prompt.md"
}
```

### Шаг 4: Настройка развертывания

#### 4.1. Настройка Docker

1. Перейдите на вкладку **"Settings"**
2. В разделе **"Build"** убедитесь, что:
   - **Build Command:** `docker build -t railway .`
   - **Start Command:** `python src/bot.py`

#### 4.2. Настройка портов

Railway.com автоматически определяет порт, но можно настроить явно:

1. В **Settings** → **Networking**
2. Установите **Port:** `8000` (или любой другой)

### Шаг 5: Запуск развертывания

1. Нажмите **"Deploy"** в верхней части панели
2. Дождитесь завершения сборки (обычно 2-5 минут)
3. Проверьте статус в разделе **"Deployments"**

## Получение токенов

### Telegram Bot Token

1. Откройте Telegram и найдите [@BotFather](https://t.me/botfather)
2. Отправьте команду `/newbot`
3. Следуйте инструкциям:
   - Введите имя бота (например: "My LLM Assistant")
   - Введите username бота (например: "my_llm_assistant_bot")
4. Скопируйте полученный токен (формат: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### OpenRouter API Key

1. Перейдите на [openrouter.ai](https://openrouter.ai)
2. Зарегистрируйтесь или войдите в аккаунт
3. Перейдите в раздел **"Keys"**
4. Нажмите **"Create Key"**
5. Скопируйте созданный API ключ
6. Пополните баланс для использования API

## Мониторинг и логи

### Просмотр логов

1. В панели Railway.com выберите ваш проект
2. Перейдите на вкладку **"Deployments"**
3. Выберите последний деплой
4. Нажмите **"View Logs"**

### Мониторинг метрик

1. Перейдите на вкладку **"Metrics"**
2. Просматривайте:
   - Использование CPU
   - Использование памяти
   - Сетевой трафик
   - Время ответа

### Проверка работоспособности

1. Откройте Telegram
2. Найдите вашего бота по username
3. Отправьте команду `/start`
4. Проверьте ответ бота

## Troubleshooting

### Частые проблемы

#### "Build failed: COPY .env ."

**Проблема:** Dockerfile пытается скопировать несуществующий файл `.env`

**Решение:**
1. Удалите строку `COPY .env .` из Dockerfile
2. Перезапустите развертывание

#### "Module not found"

**Проблема:** Отсутствуют зависимости Python

**Решение:**
1. Проверьте файл `requirements.txt`
2. Убедитесь, что все зависимости указаны
3. Перезапустите развертывание

#### "Environment variable not found"

**Проблема:** Не настроены переменные окружения

**Решение:**
1. Проверьте раздел **Variables** в Railway.com
2. Убедитесь, что все обязательные переменные добавлены
3. Проверьте правильность названий переменных

#### "Bot not responding"

**Проблема:** Бот не отвечает на сообщения

**Решение:**
1. Проверьте логи на наличие ошибок
2. Убедитесь, что `TELEGRAM_BOT_TOKEN` правильный
3. Проверьте, что бот не заблокирован в Telegram

#### "LLM API error"

**Проблема:** Ошибки при обращении к OpenRouter API

**Решение:**
1. Проверьте `OPENROUTER_API_KEY`
2. Убедитесь, что на балансе OpenRouter есть средства
3. Проверьте правильность `LLM_MODEL_NAME`

### Диагностика

#### Проверка переменных окружения

Добавьте временную переменную для отладки:

```python
# В src/config.py (временно)
import os
print("Environment variables:")
for key, value in os.environ.items():
    if key.startswith(('TELEGRAM_', 'OPENROUTER_', 'LLM_')):
        print(f"{key}: {value[:10]}..." if len(value) > 10 else f"{key}: {value}")
```

#### Проверка подключения к API

```python
# Временный тест в src/llm_client.py
async def test_connection():
    try:
        # Тест подключения к OpenRouter
        response = await client.chat.completions.create(...)
        print("OpenRouter API: OK")
    except Exception as e:
        print(f"OpenRouter API Error: {e}")
```

## Обновление развертывания

### Автоматическое обновление

Railway.com автоматически развертывает изменения при push в основную ветку:

1. Внесите изменения в код
2. Сделайте commit и push:
   ```bash
   git add .
   git commit -m "feat: новая функциональность"
   git push origin main
   ```
3. Railway.com автоматически запустит новое развертывание

### Ручное обновление

1. В панели Railway.com нажмите **"Deploy"**
2. Выберите нужную ветку или коммит
3. Нажмите **"Deploy"**

## Настройка домена

### Получение домена Railway

1. Перейдите в **Settings** → **Domains**
2. Railway автоматически предоставляет домен вида: `your-project-name.railway.app`
3. Скопируйте домен для настройки webhook (если нужно)

### Настройка webhook (опционально)

Если планируете использовать webhook вместо polling:

1. Получите домен от Railway
2. Настройте webhook в Telegram:
   ```bash
   curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
        -H "Content-Type: application/json" \
        -d '{"url": "https://your-project-name.railway.app/webhook"}'
   ```

## Безопасность

### Защита секретов

1. **Никогда не коммитьте** `.env` файл в Git
2. Используйте тип **"Secret"** для чувствительных переменных в Railway
3. Регулярно обновляйте API ключи

### Ограничение доступа

1. Настройте IP-фильтрацию в Railway (если доступно)
2. Используйте HTTPS для всех внешних соединений
3. Регулярно проверяйте логи на подозрительную активность

## Масштабирование

### Автоматическое масштабирование

Railway.com автоматически масштабирует приложение в зависимости от нагрузки.

### Ручное масштабирование

1. Перейдите в **Settings** → **Scaling**
2. Настройте:
   - **Min instances:** минимальное количество экземпляров
   - **Max instances:** максимальное количество экземпляров
   - **CPU/Memory limits:** ограничения ресурсов

## Резервное копирование

### Настройка автоматических бэкапов

1. Railway.com автоматически создает снимки состояния
2. Настройте регулярные бэкапы данных (если используете БД)
3. Экспортируйте переменные окружения для резервного копирования

### Восстановление из бэкапа

1. Создайте новый проект в Railway
2. Импортируйте переменные окружения
3. Подключите тот же Git репозиторий
4. Запустите развертывание

## Стоимость

### Тарифные планы Railway

1. **Hobby Plan** — бесплатный план с ограничениями
2. **Pro Plan** — платный план с расширенными возможностями
3. **Team Plan** — для команд

### Мониторинг расходов

1. Перейдите в **Settings** → **Usage**
2. Просматривайте использование ресурсов
3. Настройте уведомления о превышении лимитов

## Полезные команды

### Railway CLI (опционально)

```bash
# Установка Railway CLI
npm install -g @railway/cli

# Вход в аккаунт
railway login

# Подключение к проекту
railway link

# Просмотр логов
railway logs

# Запуск локально с переменными Railway
railway run python src/bot.py
```

### Git команды

```bash
# Обновление развертывания
git add .
git commit -m "feat: обновление функциональности"
git push origin main

# Откат к предыдущей версии
git revert HEAD
git push origin main
```

---

**Следующий шаг:** [Мониторинг и логирование](../operations/monitoring.md)
