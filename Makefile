.PHONY: install run logs clean test

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
