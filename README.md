# LLM-старт: Telegram-бот консультант

## Описание проекта

Telegram-бот для проведения первичных консультаций клиентов по IT-услугам компании "ТехноСервис". Бот автоматизирует процесс первичного взаимодействия с потенциальными клиентами, помогая определить подходящие услуги компании.

## Основной функционал

- 🤖 **ИИ-консультант** — обработка запросов клиентов через LLM (OpenRouter)
- 💬 **Умные диалоги** — поддержание контекста разговора
- 📞 **Сбор контактов** — непринужденный сбор данных клиентов
- 🏢 **Консультации** — помощь в выборе IT-услуг компании

## Быстрый старт

### Требования
- Python 3.11+
- Docker (опционально)
- Telegram Bot Token
- OpenRouter API Key

### Локальный запуск
```bash
# Клонирование и настройка
git clone <repository-url>
cd llmstart_project1-1
cp env.example .env
# Настройте .env файл с вашими токенами

# Установка и запуск
make install
make run
```

### Docker запуск
```bash
make docker-build
make docker-up
```

## Документация

### 🏗️ Архитектура
- [Обзор архитектуры](docs/architecture/overview.md) — компоненты и принципы
- [Детали компонентов](docs/architecture/components.md) — описание модулей

### ⚙️ Настройка
- [Быстрый старт](docs/setup/quick-start.md) — запуск за 5 минут
- [Настройка окружения](docs/setup/environment-setup.md) — детальная конфигурация
- [Интеграция с LLM](docs/setup/llm-integration.md) — настройка OpenRouter
- [Telegram Bot](docs/guides/botfather_setup.md) — создание бота

### 🚀 Развертывание
- [Локальная разработка](docs/deployment/local-development.md) — разработка и отладка
- [Docker развертывание](docs/deployment/docker-deployment.md) — контейнеризация
- [Railway.com развертывание](docs/deployment/railway-deployment.md) — облачное развертывание

### 🔧 Операции
- [Мониторинг](docs/operations/monitoring.md) — логи и метрики
- [Решение проблем](docs/operations/troubleshooting.md) — FAQ и диагностика

### 👨‍💻 Разработка
- [Стандарты кодирования](docs/development/coding-standards.md) — стиль и принципы
- [Тестирование](docs/development/testing.md) — запуск тестов

## Статус проекта

- ✅ MVP — эхо-бот + логирование
- ✅ Интеграция с LLM
- ✅ История диалогов
- ✅ Docker развертывание
- ✅ Системный промт из файла
- 🔄 Документация (в процессе)

## Автор

**Студент:** Писарев Владимир  
**Курс:** LLM-старт

## Ссылки

- [Техническое видение](docs/vision.md)
- [Идея продукта](docs/product_idea.md)
- [План разработки](docs/tasklist.md)
