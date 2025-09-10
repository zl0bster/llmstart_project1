# Мониторинг и логирование

Руководство по мониторингу работы бота и анализу логов.

## Обзор мониторинга

### Цели мониторинга
- **Отслеживание работоспособности** — бот отвечает на сообщения
- **Анализ производительности** — время ответов, использование ресурсов
- **Выявление ошибок** — проблемы с API, сетью, конфигурацией
- **Мониторинг использования** — количество запросов, расход токенов

### Ключевые метрики
- **Uptime** — время работы бота
- **Response time** — время ответа на сообщения
- **Error rate** — процент ошибок
- **Token usage** — расход токенов LLM
- **User activity** — активность пользователей

## Логирование

### Структура логов

#### Формат логов
```
2024-01-15 10:30:45,123 INFO bot.handlers: Получено сообщение от пользователя 12345
2024-01-15 10:30:45,456 INFO llm_client: LLM запрос: 1 сообщений, время ответа: 1.2s
2024-01-15 10:30:45,789 INFO bot.handlers: Отправлен ответ пользователю 12345
```

#### Уровни логирования
- **DEBUG** — отладочная информация (только для разработки)
- **INFO** — основные события (по умолчанию)
- **WARNING** — предупреждения
- **ERROR** — ошибки

### Настройка логирования

#### Базовая настройка
```python
# В src/bot.py
import logging

def setup_logging():
    """Настройка логирования."""
    config = get_config()
    
    # Создаем директорию для логов
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

#### Расширенная настройка
```python
# Расширенная настройка логирования
def setup_advanced_logging():
    """Расширенная настройка логирования."""
    config = get_config()
    
    # Создаем директорию для логов
    os.makedirs(os.path.dirname(config['LOG_FILE']), exist_ok=True)
    
    # Формат логов
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(name)s:%(lineno)d: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Файловый обработчик
    file_handler = logging.FileHandler(config['LOG_FILE'], encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    
    # Консольный обработчик
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.WARNING)
    
    # Настройка корневого логгера
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Настройка логгеров модулей
    logging.getLogger('src.handlers').setLevel(logging.INFO)
    logging.getLogger('src.llm_client').setLevel(logging.INFO)
    logging.getLogger('aiogram').setLevel(logging.WARNING)
    logging.getLogger('openai').setLevel(logging.WARNING)
```

### Что логировать

#### Основные события
```python
# В src/handlers.py
import logging

logger = logging.getLogger(__name__)

async def handle_text_message(message: Message):
    """Обработка текстовых сообщений."""
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_text = message.text
    
    # Логирование входящего сообщения
    logger.info(f"Получено сообщение от пользователя {user_id}: {user_text[:50]}...")
    
    try:
        # Генерация ответа
        response = await generate_llm_response(user_text, chat_id)
        
        # Отправка ответа
        await message.answer(response)
        
        # Логирование успешного ответа
        logger.info(f"Отправлен ответ пользователю {user_id}: {response[:50]}...")
        
    except Exception as e:
        # Логирование ошибки
        logger.error(f"Ошибка при обработке сообщения от {user_id}: {e}")
        await message.answer("Извините, произошла ошибка.")
```

#### LLM запросы
```python
# В src/llm_client.py
import logging
import time

logger = logging.getLogger(__name__)

async def generate_response(messages: List[Dict], chat_id: int) -> str:
    """Генерация ответа через LLM."""
    start_time = time.time()
    
    try:
        # Логирование запроса
        logger.info(f"LLM запрос: {len(messages)} сообщений, модель: {config['LLM_MODEL_NAME']}")
        
        # Вызов API
        response = await client.chat.completions.create(
            model=config['LLM_MODEL_NAME'],
            messages=messages,
            temperature=config['LLM_TEMPERATURE'],
            max_tokens=config['LLM_MAX_TOKENS']
        )
        
        # Расчет времени ответа
        response_time = time.time() - start_time
        
        # Логирование успешного ответа
        logger.info(f"LLM ответ: {len(response.choices[0].message.content)} символов, "
                   f"время: {response_time:.2f}s")
        
        return response.choices[0].message.content
        
    except Exception as e:
        # Логирование ошибки
        response_time = time.time() - start_time
        logger.error(f"Ошибка LLM: {e}, время: {response_time:.2f}s")
        return "Извините, произошла ошибка при обработке запроса."
```

#### Системные события
```python
# В src/bot.py
import logging

logger = logging.getLogger(__name__)

def main():
    """Главная функция запуска бота."""
    try:
        # Логирование запуска
        logger.info("Запуск бота...")
        
        # Инициализация
        setup_logging()
        config = get_config()
        logger.info("Конфигурация загружена")
        
        # Создание бота
        bot = Bot(token=config['TELEGRAM_BOT_TOKEN'])
        dp = Dispatcher(storage=MemoryStorage())
        register_handlers(dp)
        logger.info("Обработчики зарегистрированы")
        
        # Запуск
        logger.info("Бот запущен и готов к работе")
        asyncio.run(dp.start_polling(bot))
        
    except Exception as e:
        logger.error(f"Критическая ошибка при запуске бота: {e}")
        raise
    finally:
        logger.info("Бот остановлен")
```

## Анализ логов

### Просмотр логов

#### Базовые команды
```bash
# Просмотр последних записей
tail -n 100 logs/bot.log

# Просмотр в реальном времени
tail -f logs/bot.log

# Поиск ошибок
grep -i error logs/bot.log

# Поиск предупреждений
grep -i warning logs/bot.log

# Статистика по уровням
grep -c "INFO" logs/bot.log
grep -c "WARNING" logs/bot.log
grep -c "ERROR" logs/bot.log
```

#### Анализ производительности
```bash
# Время ответов LLM
grep "LLM ответ" logs/bot.log | grep -o "время: [0-9.]*s"

# Статистика запросов
grep "LLM запрос" logs/bot.log | wc -l

# Среднее время ответа
grep "LLM ответ" logs/bot.log | grep -o "время: [0-9.]*s" | sed 's/время: //' | sed 's/s//' | awk '{sum+=$1; count++} END {print sum/count}'
```

#### Анализ пользователей
```bash
# Уникальные пользователи
grep "Получено сообщение от пользователя" logs/bot.log | grep -o "пользователя [0-9]*" | sort -u

# Количество сообщений от пользователя
grep "Получено сообщение от пользователя 12345" logs/bot.log | wc -l

# Активность по времени
grep "Получено сообщение" logs/bot.log | grep -o "[0-9][0-9]:[0-9][0-9]" | sort | uniq -c
```

### Скрипты анализа

#### Анализ производительности
```python
# scripts/analyze_performance.py
import re
import statistics
from datetime import datetime

def analyze_performance(log_file):
    """Анализ производительности по логам."""
    response_times = []
    
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            # Извлечение времени ответа
            match = re.search(r'время: ([0-9.]+)s', line)
            if match:
                response_times.append(float(match.group(1)))
    
    if response_times:
        print(f"Количество запросов: {len(response_times)}")
        print(f"Среднее время ответа: {statistics.mean(response_times):.2f}s")
        print(f"Медианное время ответа: {statistics.median(response_times):.2f}s")
        print(f"Максимальное время ответа: {max(response_times):.2f}s")
        print(f"Минимальное время ответа: {min(response_times):.2f}s")
    else:
        print("Данные о производительности не найдены")

if __name__ == "__main__":
    analyze_performance("logs/bot.log")
```

#### Анализ ошибок
```python
# scripts/analyze_errors.py
import re
from collections import Counter

def analyze_errors(log_file):
    """Анализ ошибок по логам."""
    errors = []
    
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            if "ERROR" in line:
                # Извлечение сообщения об ошибке
                match = re.search(r'ERROR.*: (.*)', line)
                if match:
                    errors.append(match.group(1))
    
    if errors:
        print(f"Общее количество ошибок: {len(errors)}")
        print("\nТоп-5 ошибок:")
        error_counts = Counter(errors)
        for error, count in error_counts.most_common(5):
            print(f"  {count}x: {error}")
    else:
        print("Ошибки не найдены")

if __name__ == "__main__":
    analyze_errors("logs/bot.log")
```

## Мониторинг в реальном времени

### Health checks

#### Простой health check
```python
# scripts/health_check.py
import requests
import time
import logging

def health_check():
    """Проверка здоровья бота."""
    try:
        # Проверка файла логов
        with open("logs/bot.log", "r") as f:
            lines = f.readlines()
            last_line = lines[-1] if lines else ""
            
            # Проверка, что бот недавно писал в логи
            if "ERROR" in last_line:
                return False, "Ошибка в логах"
            
            return True, "Бот работает"
            
    except Exception as e:
        return False, f"Ошибка проверки: {e}"

if __name__ == "__main__":
    while True:
        is_healthy, message = health_check()
        status = "OK" if is_healthy else "ERROR"
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {status}: {message}")
        time.sleep(60)
```

#### Docker health check
```dockerfile
# В Dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"
```

### Мониторинг ресурсов

#### Использование памяти
```python
# scripts/monitor_resources.py
import psutil
import time
import logging

def monitor_resources():
    """Мониторинг использования ресурсов."""
    process = psutil.Process()
    
    while True:
        # Получение информации о процессе
        memory_info = process.memory_info()
        cpu_percent = process.cpu_percent()
        
        # Логирование
        logging.info(f"Использование памяти: {memory_info.rss / 1024 / 1024:.2f} MB")
        logging.info(f"Использование CPU: {cpu_percent:.2f}%")
        
        time.sleep(60)

if __name__ == "__main__":
    monitor_resources()
```

#### Мониторинг диска
```bash
# Скрипт мониторинга диска
#!/bin/bash
while true; do
    disk_usage=$(df -h logs/ | tail -1 | awk '{print $5}' | sed 's/%//')
    if [ $disk_usage -gt 80 ]; then
        echo "WARNING: Диск заполнен на $disk_usage%"
        # Ротация логов
        mv logs/bot.log logs/bot.log.old
        touch logs/bot.log
    fi
    sleep 300
done
```

## Алерты и уведомления

### Настройка алертов

#### Алерт на ошибки
```python
# scripts/error_alert.py
import smtplib
from email.mime.text import MIMEText
import logging

def send_error_alert(error_message):
    """Отправка алерта об ошибке."""
    # Настройка SMTP
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    username = "your-email@gmail.com"
    password = "your-password"
    
    # Создание сообщения
    msg = MIMEText(f"Ошибка в боте: {error_message}")
    msg['Subject'] = "Ошибка Telegram бота"
    msg['From'] = username
    msg['To'] = "admin@company.com"
    
    # Отправка
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(username, password)
        server.send_message(msg)
        server.quit()
        logging.info("Алерт отправлен")
    except Exception as e:
        logging.error(f"Ошибка отправки алерта: {e}")
```

#### Алерт на высокую нагрузку
```python
# scripts/load_alert.py
import time
import logging

def check_load():
    """Проверка нагрузки на бота."""
    # Подсчет запросов за последние 5 минут
    current_time = time.time()
    five_minutes_ago = current_time - 300
    
    request_count = 0
    with open("logs/bot.log", "r") as f:
        for line in f:
            if "LLM запрос" in line:
                # Извлечение времени из лога
                # ... логика подсчета ...
                pass
    
    # Алерт при высокой нагрузке
    if request_count > 100:  # Более 100 запросов за 5 минут
        send_load_alert(request_count)

def send_load_alert(request_count):
    """Отправка алерта о высокой нагрузке."""
    logging.warning(f"Высокая нагрузка: {request_count} запросов за 5 минут")
    # Отправка уведомления
```

### Интеграция с внешними сервисами

#### Telegram уведомления
```python
# scripts/telegram_alert.py
import asyncio
from aiogram import Bot

async def send_telegram_alert(message):
    """Отправка алерта в Telegram."""
    bot = Bot(token="YOUR_ADMIN_BOT_TOKEN")
    admin_chat_id = "YOUR_ADMIN_CHAT_ID"
    
    try:
        await bot.send_message(admin_chat_id, f"🚨 Алерт: {message}")
        await bot.session.close()
    except Exception as e:
        logging.error(f"Ошибка отправки Telegram алерта: {e}")
```

#### Webhook уведомления
```python
# scripts/webhook_alert.py
import requests
import json

def send_webhook_alert(message):
    """Отправка алерта через webhook."""
    webhook_url = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
    
    payload = {
        "text": f"🚨 Ошибка в боте: {message}",
        "channel": "#alerts",
        "username": "Bot Monitor"
    }
    
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 200:
            logging.info("Webhook алерт отправлен")
        else:
            logging.error(f"Ошибка отправки webhook: {response.status_code}")
    except Exception as e:
        logging.error(f"Ошибка отправки webhook: {e}")
```

## Ротация логов

### Настройка ротации

#### Логическая ротация
```python
# scripts/log_rotation.py
import os
import time
from datetime import datetime

def rotate_logs():
    """Ротация логов."""
    log_file = "logs/bot.log"
    
    if os.path.exists(log_file):
        # Проверка размера файла
        file_size = os.path.getsize(log_file)
        max_size = 10 * 1024 * 1024  # 10 MB
        
        if file_size > max_size:
            # Создание резервной копии
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"logs/bot_{timestamp}.log"
            
            os.rename(log_file, backup_file)
            
            # Создание нового файла логов
            open(log_file, 'a').close()
            
            logging.info(f"Логи ротированы: {backup_file}")
            
            # Удаление старых логов (старше 30 дней)
            cleanup_old_logs()

def cleanup_old_logs():
    """Очистка старых логов."""
    log_dir = "logs/"
    current_time = time.time()
    max_age = 30 * 24 * 60 * 60  # 30 дней
    
    for filename in os.listdir(log_dir):
        if filename.startswith("bot_") and filename.endswith(".log"):
            file_path = os.path.join(log_dir, filename)
            file_age = current_time - os.path.getmtime(file_path)
            
            if file_age > max_age:
                os.remove(file_path)
                logging.info(f"Удален старый лог: {filename}")

if __name__ == "__main__":
    rotate_logs()
```

#### Автоматическая ротация
```bash
# Crontab для автоматической ротации
# Ротация каждый день в 2:00
0 2 * * * /path/to/script/log_rotation.py

# Ротация при превышении размера
* * * * * /path/to/script/log_rotation.py
```

## Дашборд мониторинга

### Простой дашборд
```python
# scripts/dashboard.py
from flask import Flask, render_template
import json
import re
from datetime import datetime, timedelta

app = Flask(__name__)

def get_stats():
    """Получение статистики из логов."""
    stats = {
        'total_requests': 0,
        'error_count': 0,
        'avg_response_time': 0,
        'active_users': 0
    }
    
    # Анализ логов
    with open("logs/bot.log", "r") as f:
        for line in f:
            if "LLM запрос" in line:
                stats['total_requests'] += 1
            elif "ERROR" in line:
                stats['error_count'] += 1
    
    return stats

@app.route('/')
def dashboard():
    """Главная страница дашборда."""
    stats = get_stats()
    return render_template('dashboard.html', stats=stats)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
```

### HTML шаблон
```html
<!-- templates/dashboard.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Bot Dashboard</title>
    <meta http-equiv="refresh" content="30">
</head>
<body>
    <h1>Telegram Bot Dashboard</h1>
    
    <div class="stats">
        <div class="stat">
            <h3>Всего запросов</h3>
            <p>{{ stats.total_requests }}</p>
        </div>
        
        <div class="stat">
            <h3>Ошибки</h3>
            <p>{{ stats.error_count }}</p>
        </div>
        
        <div class="stat">
            <h3>Среднее время ответа</h3>
            <p>{{ stats.avg_response_time }}s</p>
        </div>
        
        <div class="stat">
            <h3>Активные пользователи</h3>
            <p>{{ stats.active_users }}</p>
        </div>
    </div>
</body>
</html>
```

## Полезные команды

### Мониторинг
```bash
# Просмотр логов
tail -f logs/bot.log

# Поиск ошибок
grep -i error logs/bot.log

# Статистика
grep "LLM запрос" logs/bot.log | wc -l

# Мониторинг ресурсов
top -p $(pgrep -f "python src/bot.py")
```

### Анализ
```bash
# Анализ производительности
python scripts/analyze_performance.py

# Анализ ошибок
python scripts/analyze_errors.py

# Health check
python scripts/health_check.py
```

---

**Следующий шаг:** [Решение проблем](troubleshooting.md)
