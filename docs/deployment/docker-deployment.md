# Docker развертывание

Руководство по контейнеризации и развертыванию бота в Docker.

## Обзор Docker развертывания

Docker обеспечивает изолированное окружение для запуска бота, упрощая развертывание и масштабирование.

### Преимущества
- **Изоляция** — независимое окружение
- **Портабельность** — работает везде, где есть Docker
- **Масштабируемость** — легко запускать несколько экземпляров
- **Управление зависимостями** — все зависимости в контейнере

## Структура Docker файлов

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Копирование зависимостей и установка
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY src/ ./src/
COPY .env .

# Создание директорий для логов и данных
RUN mkdir -p logs data

# Точка входа
CMD ["python", "src/bot.py"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  telegram-bot:
    build: .
    container_name: llmstart-bot
    env_file:
      - .env
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c", "import sys; sys.exit(0)"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### .dockerignore
```
# Виртуальное окружение
.venv/
venv/

# Git
.git/
.gitignore

# Логи
logs/*.log

# Кэш Python
__pycache__/
*.pyc
*.pyo

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Документация (опционально)
docs/
README.md
```

## Сборка образа

### Базовая сборка
```bash
# Сборка образа
docker build -t llmstart-bot .

# Сборка с тегом версии
docker build -t llmstart-bot:v1.0.0 .

# Сборка без кэша
docker build --no-cache -t llmstart-bot .
```

### Через Make
```bash
# Сборка образа
make docker-build

# Сборка с прогрессом
make docker-build
```

### Оптимизация сборки
```dockerfile
# Многоэтапная сборка для уменьшения размера
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY src/ ./src/
COPY .env .

RUN mkdir -p logs data

# Добавляем локальные пакеты в PATH
ENV PATH=/root/.local/bin:$PATH

CMD ["python", "src/bot.py"]
```

## Запуск контейнера

### Базовый запуск
```bash
# Запуск контейнера
docker run -d --name llmstart-bot --env-file .env llmstart-bot

# Запуск с томами
docker run -d --name llmstart-bot \
  --env-file .env \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/data:/app/data \
  llmstart-bot
```

### Через docker-compose
```bash
# Запуск в фоне
docker-compose up -d

# Запуск с логами
docker-compose up

# Перезапуск
docker-compose restart
```

### Через Make
```bash
# Запуск контейнера
make docker-up

# Просмотр логов
make docker-logs

# Остановка
make docker-down
```

## Управление контейнерами

### Основные команды
```bash
# Просмотр запущенных контейнеров
docker ps

# Просмотр всех контейнеров
docker ps -a

# Просмотр логов
docker logs llmstart-bot

# Просмотр логов в реальном времени
docker logs -f llmstart-bot

# Остановка контейнера
docker stop llmstart-bot

# Удаление контейнера
docker rm llmstart-bot

# Перезапуск контейнера
docker restart llmstart-bot
```

### Вход в контейнер
```bash
# Вход в запущенный контейнер
docker exec -it llmstart-bot bash

# Выполнение команды в контейнере
docker exec llmstart-bot python -c "print('Hello from container')"

# Просмотр файлов в контейнере
docker exec llmstart-bot ls -la /app
```

## Мониторинг и логи

### Просмотр логов
```bash
# Логи контейнера
docker logs llmstart-bot

# Логи с временными метками
docker logs -t llmstart-bot

# Последние 100 строк
docker logs --tail 100 llmstart-bot

# Логи в реальном времени
docker logs -f llmstart-bot
```

### Мониторинг ресурсов
```bash
# Использование ресурсов
docker stats llmstart-bot

# Детальная информация о контейнере
docker inspect llmstart-bot

# Процессы в контейнере
docker top llmstart-bot
```

### Health checks
```yaml
# В docker-compose.yml
healthcheck:
  test: ["CMD", "python", "-c", "import sys; sys.exit(0)"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

## Переменные окружения

### Настройка через .env
```env
# Telegram Bot Token
TELEGRAM_BOT_TOKEN=your_bot_token_here

# OpenRouter API Key
OPENROUTER_API_KEY=your_api_key_here

# Настройки для продакшна
LOG_LEVEL=INFO
LOG_FILE=logs/bot.log
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=500
HISTORY_MAX_TURNS=5
```

### Переменные для разных сред
```bash
# Разработка
docker run --env-file .env.development llmstart-bot

# Продакшн
docker run --env-file .env.production llmstart-bot

# Тестирование
docker run --env-file .env.testing llmstart-bot
```

### Переменные в docker-compose
```yaml
services:
  telegram-bot:
    build: .
    environment:
      - LOG_LEVEL=INFO
      - LLM_TEMPERATURE=0.7
    env_file:
      - .env
```

## Тома и персистентность

### Настройка томов
```yaml
# В docker-compose.yml
volumes:
  - ./logs:/app/logs
  - ./data:/app/data
  - ./docs:/app/docs
```

### Управление данными
```bash
# Создание именованного тома
docker volume create llmstart-logs

# Использование именованного тома
docker run -v llmstart-logs:/app/logs llmstart-bot

# Просмотр томов
docker volume ls

# Удаление тома
docker volume rm llmstart-logs
```

## Сетевые настройки

### Настройка сети
```yaml
# В docker-compose.yml
networks:
  bot-network:
    driver: bridge

services:
  telegram-bot:
    networks:
      - bot-network
```

### Проброс портов
```yaml
# Если нужен webhook
services:
  telegram-bot:
    ports:
      - "8080:8080"
```

## Масштабирование

### Запуск нескольких экземпляров
```bash
# Запуск 3 экземпляров
docker-compose up --scale telegram-bot=3

# Или через docker run
docker run -d --name llmstart-bot-1 --env-file .env llmstart-bot
docker run -d --name llmstart-bot-2 --env-file .env llmstart-bot
docker run -d --name llmstart-bot-3 --env-file .env llmstart-bot
```

### Load balancer
```yaml
# docker-compose.yml с nginx
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - telegram-bot

  telegram-bot:
    build: .
    env_file:
      - .env
    scale: 3
```

## Безопасность

### Запуск без root
```dockerfile
# Создание пользователя
RUN adduser --disabled-password --gecos '' botuser

# Переключение на пользователя
USER botuser

# Установка прав
RUN chown -R botuser:botuser /app
```

### Ограничение ресурсов
```yaml
# В docker-compose.yml
services:
  telegram-bot:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

### Секреты
```yaml
# Использование Docker secrets
services:
  telegram-bot:
    secrets:
      - telegram_token
      - openrouter_key

secrets:
  telegram_token:
    file: ./secrets/telegram_token.txt
  openrouter_key:
    file: ./secrets/openrouter_key.txt
```

## CI/CD интеграция

### GitHub Actions
```yaml
# .github/workflows/docker.yml
name: Docker Build and Deploy

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build Docker image
        run: docker build -t llmstart-bot .
      
      - name: Run tests
        run: docker run --rm llmstart-bot python -m pytest tests/
      
      - name: Deploy
        run: |
          docker tag llmstart-bot:latest your-registry/llmstart-bot:latest
          docker push your-registry/llmstart-bot:latest
```

### Автоматическое развертывание
```bash
# Скрипт развертывания
#!/bin/bash
set -e

echo "Building image..."
docker build -t llmstart-bot .

echo "Stopping old container..."
docker stop llmstart-bot || true
docker rm llmstart-bot || true

echo "Starting new container..."
docker run -d --name llmstart-bot --env-file .env llmstart-bot

echo "Deployment complete!"
```

## Troubleshooting

### Частые проблемы

#### "Container won't start"
```bash
# Проверьте логи
docker logs llmstart-bot

# Проверьте конфигурацию
docker run --rm --env-file .env llmstart-bot python -c "from src.config import get_config; print(get_config())"
```

#### "Permission denied"
```bash
# Проверьте права на файлы
ls -la logs/ data/

# Исправьте права
chmod 755 logs/ data/
```

#### "Out of memory"
```bash
# Проверьте использование памяти
docker stats llmstart-bot

# Увеличьте лимиты
docker run --memory=1g llmstart-bot
```

#### "Network issues"
```bash
# Проверьте сеть
docker network ls
docker network inspect bridge

# Пересоздайте сеть
docker network prune
```

### Диагностика
```bash
# Проверка здоровья контейнера
docker inspect llmstart-bot | grep Health

# Проверка процессов
docker exec llmstart-bot ps aux

# Проверка файловой системы
docker exec llmstart-bot df -h
```

## Очистка

### Очистка контейнеров
```bash
# Остановка и удаление контейнера
docker stop llmstart-bot
docker rm llmstart-bot

# Удаление всех остановленных контейнеров
docker container prune
```

### Очистка образов
```bash
# Удаление образа
docker rmi llmstart-bot

# Удаление неиспользуемых образов
docker image prune
```

### Полная очистка
```bash
# Очистка всего
docker system prune -a

# Или через Make
make docker-clean
```

## Полезные команды

### Make команды
```bash
# Сборка образа
make docker-build

# Запуск контейнера
make docker-up

# Просмотр логов
make docker-logs

# Остановка контейнера
make docker-down

# Полный перезапуск
make docker-restart

# Очистка
make docker-clean
```

### Docker команды
```bash
# Сборка
docker build -t llmstart-bot .

# Запуск
docker run -d --name llmstart-bot --env-file .env llmstart-bot

# Логи
docker logs -f llmstart-bot

# Остановка
docker stop llmstart-bot

# Удаление
docker rm llmstart-bot
```

---

**Следующий шаг:** [Мониторинг и логирование](../operations/monitoring.md)
