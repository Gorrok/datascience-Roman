#!/bin/bash

echo "🔧 Исправляем боты на сервере..."

# Исправляем Invite Tracker
cd /root/invite_bot
sed -i 's/async def main()/def main()/' invite_tracker.py
echo "✅ Invite Tracker исправлен"

# Создаем Member Tracker
cd "/root/beget_deployment 2"

cat > bot.py << 'BOT_EOF'
import os
import asyncio
import sys
from datetime import datetime
from typing import List, Optional

from telegram import Update, ChatMember, ChatMemberUpdated
from telegram.ext import (
    Application,
    ChatMemberHandler,
    CommandHandler,
    ContextTypes,
)
from dotenv import load_dotenv
from loguru import logger

from models import ChannelMember, MemberActivity
from sheets_manager import GoogleSheetsManager

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'logs/bot.log')

# Создаем директорию для логов
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logger.add(LOG_FILE, level=LOG_LEVEL, rotation="1 day", retention="7 days")
logger.add(sys.stdout, level=LOG_LEVEL)

# Настройка Google Sheets
sheets_manager = None

class MemberTrackerBot:
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.monitored_channels = self._parse_channels(os.getenv('MONITORED_CHANNELS', ''))

        # Настройки Google Sheets
        self.credentials_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH', 'credentials.json')
        self.spreadsheet_id = os.getenv('GOOGLE_SHEETS_SPREADSHEET_ID')
        self.members_sheet_name = os.getenv('GOOGLE_SHEETS_MEMBERS_SHEET', 'members')
        self.activity_sheet_name = os.getenv('GOOGLE_SHEETS_ACTIVITY_SHEET', 'activity')

        if not self.bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN не найден")

        if not self.spreadsheet_id:
            raise ValueError("GOOGLE_SHEETS_SPREADSHEET_ID не найден")

        logger.info(f"Member Tracker инициализирован")

    def _parse_channels(self, channels_str: str) -> List[str]:
        if not channels_str:
            return []
        return [channel.strip() for channel in channels_str.split(',') if channel.strip()]

    async def init_sheets(self):
        global sheets_manager
        sheets_manager = GoogleSheetsManager(
            credentials_path=self.credentials_path,
            spreadsheet_id=self.spreadsheet_id
        )
        await sheets_manager.initialize()
        sheets_manager.setup_sheets(self.members_sheet_name, self.activity_sheet_name)
        logger.info("Google Sheets инициализирован")

    async def handle_chat_member_update(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.chat_member:
            return
        chat_member_update: ChatMemberUpdated = update.chat_member
        chat = chat_member_update.chat
        new_member: ChatMember = chat_member_update.new_chat_member
        old_member: ChatMember = chat_member_update.old_chat_member

        if chat.username not in self.monitored_channels:
            return

        logger.info(f"Member update: @{chat.username} {old_member.status} -> {new_member.status}")

        activity_type = self._get_activity_type(old_member, new_member)
        if activity_type:
            await self._save_member_info(chat, new_member.user, new_member.status, activity_type)

    def _get_activity_type(self, old_member: ChatMember, new_member: ChatMember) -> Optional[str]:
        old_status = old_member.status
        new_status = new_member.status

        if old_status in ['left', 'kicked', 'banned'] and new_status in ['member', 'administrator', 'creator']:
            return 'joined'
        elif old_status in ['member', 'administrator', 'creator'] and new_status in ['left', 'kicked', 'banned']:
            return 'left'
        return None

    async def _save_member_info(self, chat, user, status: str, activity_type: str):
        global sheets_manager
        if not sheets_manager:
            return

        if activity_type == 'joined':
            new_member = ChannelMember(
                user_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                channel_username=chat.username,
                joined_at=datetime.utcnow(),
                left_at=None,
                is_active=True,
                status=status
            )
            sheets_manager.save_member(new_member)
            logger.info(f"Member saved: {user.id}")

    async def run(self):
        await self.init_sheets()
        application = Application.builder().token(self.bot_token).build()
        application.add_handler(ChatMemberHandler(self.handle_chat_member_update, ChatMemberHandler.CHAT_MEMBER))
        logger.info("Member Tracker started")
        await application.run_polling()

async def main():
    bot = MemberTrackerBot()
    await bot.run()

if __name__ == '__main__':
    asyncio.run(main())
BOT_EOF

echo "✅ Member Tracker создан"

# Проверяем файлы
cd "/root/beget_deployment 2"
ls -la bot.py
python3 -m py_compile bot.py && echo "✅ Member Tracker скомпилирован"

cd /root/invite_bot
python3 -m py_compile invite_tracker.py && echo "✅ Invite Tracker скомпилирован"

echo "🎉 Исправление завершено!"
