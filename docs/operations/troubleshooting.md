# Решение проблем и FAQ

Руководство по диагностике и решению проблем с Telegram-ботом.

## Быстрая диагностика

### Проверка статуса системы
```bash
# Проверка запуска бота
ps aux | grep python

# Проверка логов
tail -f logs/bot.log

# Проверка конфигурации
python -c "from src.config import get_config; print('Config OK')"
```

### Основные команды диагностики
```bash
# Проверка зависимостей
pip list

# Проверка импортов
python -c "import aiogram, openai; print('Imports OK')"

# Проверка токенов
python -c "from src.config import get_config; config = get_config(); print('Tokens OK' if config['TELEGRAM_BOT_TOKEN'] and config['OPENROUTER_API_KEY'] else 'Tokens MISSING')"
```

## Частые проблемы

### 1. Ошибки конфигурации

#### "TELEGRAM_BOT_TOKEN не найден"
**Симптомы:**
```
ValueError: TELEGRAM_BOT_TOKEN не найден в переменных окружения
```

**Решение:**
```bash
# Проверьте файл .env
cat .env | grep TELEGRAM_BOT_TOKEN

# Убедитесь, что файл существует
ls -la .env

# Проверьте, что токен скопирован полностью
echo $TELEGRAM_BOT_TOKEN
```

**Проверка токена:**
```bash
# Тест токена через API
curl "https://api.telegram.org/bot<YOUR_TOKEN>/getMe"
```

#### "OPENROUTER_API_KEY не найден"
**Симптомы:**
```
ValueError: OPENROUTER_API_KEY не найден в переменных окружения
```

**Решение:**
```bash
# Проверьте файл .env
cat .env | grep OPENROUTER_API_KEY

# Проверьте, что ключ начинается с sk-or-v1-
grep "sk-or-v1-" .env
```

**Проверка ключа:**
```bash
# Тест API ключа
python -c "
from openai import OpenAI
from src.config import get_config
config = get_config()
client = OpenAI(api_key=config['OPENROUTER_API_KEY'], base_url=config['OPENROUTER_API_URL'])
print('API Key OK')
"
```

### 2. Ошибки сети

#### "Connection timeout"
**Симптомы:**
```
openai.APITimeoutError: Request timed out
```

**Решение:**
```bash
# Проверьте интернет-соединение
ping google.com

# Проверьте доступность OpenRouter
ping openrouter.ai

# Проверьте прокси/файрвол
curl -I https://openrouter.ai/api/v1/models
```

#### "SSL Certificate Error"
**Симптомы:**
```
ssl.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED]
```

**Решение:**
```bash
# Обновите сертификаты
pip install --upgrade certifi

# Или отключите проверку SSL (не рекомендуется)
export PYTHONHTTPSVERIFY=0
```

### 3. Ошибки LLM

#### "Model not found"
**Симптомы:**
```
openai.NotFoundError: The model 'invalid-model' does not exist
```

**Решение:**
```bash
# Проверьте доступные модели
python -c "
from openai import OpenAI
from src.config import get_config
config = get_config()
client = OpenAI(api_key=config['OPENROUTER_API_KEY'], base_url=config['OPENROUTER_API_URL'])
models = client.models.list()
for model in models.data[:5]:
    print(model.id)
"

# Используйте правильное название модели
echo "LLM_MODEL_NAME=openai/gpt-3.5-turbo" >> .env
```

#### "Rate limit exceeded"
**Симптомы:**
```
openai.RateLimitError: Rate limit exceeded
```

**Решение:**
```bash
# Проверьте лимиты в OpenRouter
# Увеличьте задержки между запросами
# Рассмотрите upgrade плана
```

#### "Context length exceeded"
**Симптомы:**
```
openai.BadRequestError: Context length exceeded
```

**Решение:**
```bash
# Уменьшите размер истории
echo "HISTORY_MAX_TURNS=3" >> .env

# Уменьшите максимальные токены
echo "LLM_MAX_TOKENS=200" >> .env

# Сократите системный промт
```

### 4. Ошибки Telegram

#### "Unauthorized"
**Симптомы:**
```
aiogram.exceptions.TelegramUnauthorizedError: Unauthorized
```

**Решение:**
```bash
# Проверьте токен бота
curl "https://api.telegram.org/bot<YOUR_TOKEN>/getMe"

# Убедитесь, что бот не заблокирован
# Проверьте, что токен скопирован полностью
```

#### "Bad Request"
**Симптомы:**
```
aiogram.exceptions.TelegramBadRequest: Bad Request
```

**Решение:**
```bash
# Проверьте формат сообщений
# Убедитесь, что сообщения не слишком длинные
# Проверьте, что бот не заблокирован пользователем
```

### 5. Ошибки Python

#### "Module not found"
**Симптомы:**
```
ModuleNotFoundError: No module named 'aiogram'
```

**Решение:**
```bash
# Активируйте виртуальное окружение
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Установите зависимости
pip install -r requirements.txt

# Проверьте установку
pip list | grep aiogram
```

#### "Import error"
**Симптомы:**
```
ImportError: cannot import name 'Bot' from 'aiogram'
```

**Решение:**
```bash
# Проверьте версию aiogram
pip show aiogram

# Обновите до правильной версии
pip install aiogram==3.0.0

# Проверьте совместимость версий
pip check
```

## Диагностика производительности

### Мониторинг ресурсов
```bash
# Использование CPU и памяти
top -p $(pgrep -f "python src/bot.py")

# Использование диска
df -h

# Использование сети
netstat -i
```

### Анализ логов
```bash
# Поиск ошибок
grep -i error logs/bot.log

# Поиск предупреждений
grep -i warning logs/bot.log

# Статистика запросов
grep "LLM запрос" logs/bot.log | wc -l

# Время ответов
grep "время ответа" logs/bot.log
```

### Профилирование
```python
# Добавьте в код для профилирования
import cProfile
import pstats

def profile_function(func):
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        stats.print_stats(10)
        return result
    return wrapper
```

## Восстановление после сбоев

### Автоматический перезапуск
```bash
# Скрипт мониторинга
#!/bin/bash
while true; do
    if ! pgrep -f "python src/bot.py" > /dev/null; then
        echo "Bot is down, restarting..."
        python src/bot.py &
    fi
    sleep 30
done
```

### Резервное копирование
```bash
# Создание бэкапа
tar -czf backup-$(date +%Y%m%d).tar.gz src/ docs/ .env

# Восстановление из бэкапа
tar -xzf backup-20240115.tar.gz
```

### Восстановление конфигурации
```bash
# Восстановление .env из примера
cp env.example .env

# Редактирование конфигурации
nano .env
```

## FAQ

### Вопросы по настройке

**Q: Как получить токен Telegram бота?**
A: Найдите @BotFather в Telegram, отправьте `/newbot`, следуйте инструкциям.

**Q: Как получить API ключ OpenRouter?**
A: Зарегистрируйтесь на openrouter.ai, перейдите в раздел "Keys", создайте новый ключ.

**Q: Какая модель LLM лучше?**
A: Для быстрых ответов - gpt-3.5-turbo, для качества - gpt-4, для экономии - claude-3-haiku.

**Q: Как настроить системный промт?**
A: Отредактируйте файл `docs/system_prompt.md` под ваши нужды.

### Вопросы по производительности

**Q: Бот отвечает медленно?**
A: Уменьшите `LLM_MAX_TOKENS`, используйте быструю модель, уменьшите `HISTORY_MAX_TURNS`.

**Q: Высокие расходы на API?**
A: Уменьшите `HISTORY_MAX_TURNS`, используйте дешевую модель, оптимизируйте промт.

**Q: Бот потребляет много памяти?**
A: Уменьшите `HISTORY_MAX_TURNS`, перезапускайте бота периодически.

### Вопросы по развертыванию

**Q: Как запустить бота в фоне?**
A: Используйте `nohup python src/bot.py &` или Docker.

**Q: Как обновить бота без остановки?**
A: Используйте Docker с rolling update или blue-green deployment.

**Q: Как масштабировать бота?**
A: Запустите несколько экземпляров с load balancer.

## Полезные команды

### Диагностика
```bash
# Проверка статуса
make logs

# Проверка конфигурации
python -c "from src.config import get_config; print(get_config())"

# Тест API
python -c "from src.llm_client import load_system_prompt; print('Prompt OK')"
```

### Восстановление
```bash
# Перезапуск бота
make docker-restart

# Очистка логов
rm logs/bot.log

# Переустановка зависимостей
make clean && make install
```

### Мониторинг
```bash
# Просмотр логов
tail -f logs/bot.log

# Статистика
grep "INFO" logs/bot.log | wc -l

# Ошибки
grep "ERROR" logs/bot.log
```

## Контакты поддержки

### Внутренняя поддержка
- **Документация:** [README.md](../../README.md)
- **Архитектура:** [docs/architecture/overview.md](../architecture/overview.md)
- **Настройка:** [docs/setup/quick-start.md](../setup/quick-start.md)

### Внешняя поддержка
- **Telegram Bot API:** [@BotFather](https://t.me/BotFather)
- **OpenRouter:** [support@openrouter.ai](mailto:support@openrouter.ai)
- **aiogram:** [GitHub Issues](https://github.com/aiogram/aiogram/issues)

---

**Следующий шаг:** [Стандарты кодирования](../development/coding-standards.md)
