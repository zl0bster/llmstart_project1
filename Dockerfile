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
