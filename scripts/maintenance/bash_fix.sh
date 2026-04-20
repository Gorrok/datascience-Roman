#!/bin/bash

echo "🔧 Финальное исправление ботов..."

# Создаем .env для Invite Tracker
cat > /root/invite_bot/.env << 'ENV_EOF'
# Настройки бота для Beget
TELEGRAM_BOT_TOKEN=8566507218:AAEG5ifQrdlvMH3cWA5eMSRW6p7wacIAy10
MONITORED_CHANNELS=@ваш_канал
GOOGLE_SHEETS_CREDENTIALS_PATH=credentials.json
GOOGLE_SHEETS_SPREADSHEET_ID=ShepoitBukmekera
GOOGLE_SHEETS_MEMBERS_SHEET=Members
GOOGLE_SHEETS_ACTIVITY_SHEET=Links
LOG_LEVEL=INFO
LOG_FILE=logs/bot.log
ENV_EOF

# Создаем .env для Member Tracker
cat > "/root/beget_deployment 2/.env" << 'ENV_EOF'
# Настройки бота для Beget
TELEGRAM_BOT_TOKEN=8566507218:AAEG5ifQrdlvMH3cWA5eMSRW6p7wacIAy10
MONITORED_CHANNELS=@ваш_канал
GOOGLE_SHEETS_CREDENTIALS_PATH=credentials1.json
GOOGLE_SHEETS_SPREADSHEET_ID=ShepoitBukmekera
GOOGLE_SHEETS_MEMBERS_SHEET=members
GOOGLE_SHEETS_ACTIVITY_SHEET=activity
LOG_LEVEL=INFO
LOG_FILE=logs/bot.log
ENV_EOF

# Создаем Member Tracker
cat > "/root/beget_deployment 2/bot.py" << 'BOT_EOF'
import os
import asyncio
from telegram import Update, ChatMember, ChatMemberUpdated
from telegram.ext import Application, ChatMemberHandler, ContextTypes
from dotenv import load_dotenv
from loguru import logger
from datetime import datetime

load_dotenv()
logger.add('logs/bot.log', level='INFO')

class SimpleBot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.channels = ["ваш_канал"]
    
    async def handle_update(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.chat_member:
            logger.info('Member update received')
    
    async def run(self):
        app = Application.builder().token(self.token).build()
        app.add_handler(ChatMemberHandler(self.handle_update, ChatMemberHandler.CHAT_MEMBER))
        logger.info('Simple Member Tracker started')
        await app.run_polling()

async def main():
    bot = SimpleBot()
    await bot.run()

if __name__ == '__main__':
    asyncio.run(main())
BOT_EOF

echo "✅ Файлы созданы"

# Проверяем
echo "=== ПРОВЕРКА ФАЙЛОВ ==="
ls -la /root/invite_bot/.env
ls -la "/root/beget_deployment 2/.env"
ls -la "/root/beget_deployment 2/bot.py"

echo "=== ТЕСТ КОМПИЛЯЦИИ ==="
cd /root/invite_bot && python3 -m py_compile invite_tracker.py && echo "✅ Invite OK"
cd "/root/beget_deployment 2" && python3 -m py_compile bot.py && echo "✅ Member OK"

echo "🎉 Исправление завершено!"
