#!/bin/bash

echo "🔧 Ремонт ботов на сервере..."

# Исправляем Invite Tracker
cd /root/invite_bot
sed -i 's/def main()/async def main()/' invite_tracker.py
echo "✅ Invite Tracker исправлен"

# Создаем Member Tracker
cd "/root/beget_deployment 2"
cat > bot.py << 'BOT_EOF'
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

echo "✅ Member Tracker создан"

# Проверяем
cd "/root/beget_deployment 2"
python3 -m py_compile bot.py && echo "✅ Member OK" || echo "❌ Member error"

cd /root/invite_bot
python3 -m py_compile invite_tracker.py && echo "✅ Invite OK" || echo "❌ Invite error"

echo "🎉 Ремонт завершен!"
