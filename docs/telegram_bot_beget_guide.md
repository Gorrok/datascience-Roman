# Инструкция по запуску Telegram бота на Beget

## 1. Структура файлов на хостинге

Создайте такую структуру файлов в корне вашего сайта:

```
/your-domain.ru/
├── bot.py              # Основной файл бота
├── requirements.txt    # Список зависимостей
├── .env               # Переменные окружения (API ключи)
├── logs/              # Папка для логов
└── data/              # Папка для данных (БД, файлы)
```

## 2. Файл requirements.txt

```txt
python-telegram-bot==20.7
python-dotenv==1.0.0
sqlalchemy==2.0.23
aiosqlite==0.19.0
```

## 3. Файл .env

```env
TELEGRAM_BOT_TOKEN=ваш_токен_бота
TELEGRAM_API_ID=ваш_api_id
TELEGRAM_API_HASH=ваш_api_hash
DATABASE_URL=sqlite:///data/bot_database.db
```

## 4. Основной файл бота (bot.py)

```python
import os
import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('logs/bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Настройка базы данных
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite+aiosqlite:///data/bot_database.db')
engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, class_=Session, expire_on_commit=False)

# Здесь будет ваш код бота для отслеживания вступлений в канал
# ...

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Бот запущен!')

async def main():
    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

    application.add_handler(CommandHandler("start", start))
    # Добавьте здесь обработчики для отслеживания вступлений в канал

    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
```

## 5. Запуск бота на Beget

### Через SSH (рекомендуется):

```bash
# Подключитесь к серверу по SSH
ssh ваш_логин@ваш_домен.ru

# Перейдите в директорию сайта
cd /home/ваш_логин/ваш_домен.ru

# Создайте виртуальное окружение
python3 -m venv bot_env
source bot_env/bin/activate

# Установите зависимости
pip install -r requirements.txt

# Запустите бота в фоне
nohup python bot.py > logs/bot_output.log 2>&1 &
```

### Через cron для автозапуска:

```bash
# Отредактируйте crontab
crontab -e

# Добавьте строку для автозапуска при перезагрузке
@reboot cd /home/ваш_логин/ваш_домен.ru && source bot_env/bin/activate && nohup python bot.py > logs/bot_output.log 2>&1 &
```

## 6. Мониторинг и поддержка

### Проверка статуса бота:
```bash
ps aux | grep python
```

### Просмотр логов:
```bash
tail -f logs/bot.log
```

### Перезапуск бота:
```bash
pkill -f bot.py
source bot_env/bin/activate
nohup python bot.py > logs/bot_output.log 2>&1 &
```

## 7. Особенности Beget

- **Ограничения по времени**: Долгоживущие процессы могут быть прерваны
- **Ресурсы**: Ограниченная память и CPU
- **База данных**: Используйте SQLite или подключитесь к внешней БД
- **Webhook**: Для production используйте webhook вместо polling

## 8. Безопасность

- Не храните API ключи в коде
- Используйте .env файл для конфиденциальных данных
- Регулярно обновляйте зависимости
- Настройте правильные права доступа к файлам
