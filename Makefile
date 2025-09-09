.PHONY: install run logs clean test docker-build docker-up docker-down docker-logs docker-clean docker-restart

# Docker настройки
DOCKER_HOST ?= tcp://localhost:2375

# Установка зависимостей
install:
	python -m venv .venv
	.venv\Scripts\activate && pip install -r requirements.txt

# Запуск бота
run:
	.venv\Scripts\activate && python src/bot.py

# Просмотр логов
logs:
	tail -f logs/bot.log

# Очистка
clean:
	rm -rf .venv logs/*.log

# Тестирование
test:
	.venv\Scripts\activate && python -m pytest tests/

# Docker команды
docker-build:
	@echo "🔨 Сборка Docker образа..."
	set DOCKER_HOST=$(DOCKER_HOST) && docker compose build --progress=plain
	@echo "✅ Образ собран успешно"

docker-up:
	@echo "🚀 Запуск контейнера..."
	set DOCKER_HOST=$(DOCKER_HOST) && docker compose up -d
	@echo "✅ Контейнер запущен"

docker-down:
	@echo "⏹️ Остановка контейнера..."
	set DOCKER_HOST=$(DOCKER_HOST) && docker compose down
	@echo "✅ Контейнер остановлен"

docker-logs:
	@echo "📋 Просмотр логов (Ctrl+C для выхода)..."
	set DOCKER_HOST=$(DOCKER_HOST) && docker compose logs -f

docker-clean:
	@echo "🧹 Очистка контейнеров и образов..."
	set DOCKER_HOST=$(DOCKER_HOST) && docker compose down -v
	set DOCKER_HOST=$(DOCKER_HOST) && docker system prune -f
	@echo "✅ Очистка завершена"

# Полный перезапуск
docker-restart: docker-down docker-build docker-up
	@echo "🔄 Перезапуск завершен"
