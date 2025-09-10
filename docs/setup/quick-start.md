# Быстрый старт

Запустите Telegram-бота консультанта за 5 минут.

## Предварительные требования

- **Python 3.11+** — [скачать](https://www.python.org/downloads/)
- **Git** — [скачать](https://git-scm.com/downloads)
- **Docker** (опционально) — [скачать](https://www.docker.com/get-started)

## Шаг 1: Клонирование проекта

```bash
git clone <repository-url>
cd llmstart_project1-1
```

## Шаг 2: Настройка окружения

### Создание .env файла
```bash
cp env.example .env
```

### Редактирование .env
Откройте файл `.env` и заполните обязательные параметры:

```env
# Telegram Bot Token (получен от BotFather)
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# LLM настройки (OpenRouter)
OPENROUTER_API_KEY=sk-or-v1-your-api-key-here

# Остальные настройки можно оставить по умолчанию
LOG_LEVEL=INFO
LOG_FILE=logs/bot.log
LLM_MODEL_NAME=openai/gpt-3.5-turbo
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=500
HISTORY_MAX_TURNS=5
```

## Шаг 3: Получение токенов

### Telegram Bot Token
1. Найдите [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте полученный токен в `.env`

### OpenRouter API Key
1. Зарегистрируйтесь на [OpenRouter](https://openrouter.ai/)
2. Перейдите в раздел "Keys"
3. Создайте новый API ключ
4. Скопируйте ключ в `.env`

## Шаг 4: Установка зависимостей

### Локальная установка
```bash
# Создание виртуального окружения
python -m venv .venv

# Активация (Windows)
.venv\Scripts\activate

# Активация (Linux/Mac)
source .venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt
```

### Или через Make
```bash
make install
```

## Шаг 5: Запуск бота

### Локальный запуск
```bash
# Активируйте виртуальное окружение
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Запуск бота
python src/bot.py
```

### Или через Make
```bash
make run
```

### Docker запуск
```bash
# Сборка образа
make docker-build

# Запуск контейнера
make docker-up
```

## Шаг 6: Проверка работы

1. Найдите вашего бота в Telegram по username
2. Отправьте команду `/start`
3. Бот должен ответить приветствием
4. Отправьте любое сообщение
5. Бот должен ответить через LLM

## Ожидаемый результат

```
2024-01-15 10:30:45 INFO bot: Логирование настроено
2024-01-15 10:30:45 INFO bot: Конфигурация загружена
2024-01-15 10:30:45 INFO bot: Обработчики зарегистрированы
2024-01-15 10:30:45 INFO bot: Бот запущен
```

## Возможные проблемы

### Ошибка "TELEGRAM_BOT_TOKEN не найден"
- Проверьте файл `.env`
- Убедитесь, что токен скопирован полностью
- Проверьте, что нет лишних пробелов

### Ошибка "OpenRouter API недоступен"
- Проверьте `OPENROUTER_API_KEY` в `.env`
- Убедитесь, что у вас есть доступ к интернету
- Проверьте баланс на OpenRouter

### Бот не отвечает
- Проверьте логи в файле `logs/bot.log`
- Убедитесь, что бот запущен
- Проверьте, что токен правильный

## Следующие шаги

После успешного запуска:

1. **[Детальная настройка](environment-setup.md)** — полная конфигурация
2. **[Настройка LLM](llm-integration.md)** — оптимизация параметров
3. **[Локальная разработка](../deployment/local-development.md)** — отладка и разработка
4. **[Docker развертывание](../deployment/docker-deployment.md)** — контейнеризация

## Полезные команды

```bash
# Просмотр логов
make logs

# Остановка Docker контейнера
make docker-down

# Очистка
make clean

# Запуск тестов
make test
```

---

**Время выполнения:** ~5 минут  
**Сложность:** Начальный уровень
