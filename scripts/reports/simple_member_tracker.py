import os
import asyncio
import sys
from datetime import datetime
from typing import List, Optional

from telegram import Update, ChatMember, ChatMemberUpdated
from telegram.ext import (
    Application,
    ChatMemberHandler,
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
            raise ValueError("TELEGRAM_BOT_TOKEN не найден в переменных окружения")

        if not self.spreadsheet_id:
            raise ValueError("GOOGLE_SHEETS_SPREADSHEET_ID не найден в переменных окружения")

        logger.info(f"Инициализация бота. Мониторинг каналов: {self.monitored_channels}")
        logger.info(f"Google Sheets ID: {self.spreadsheet_id}")

    def _parse_channels(self, channels_str: str) -> List[str]:
        """Парсит строку с каналами в список"""
        if not channels_str:
            return []
        return [channel.strip() for channel in channels_str.split(',') if channel.strip()]

    async def init_sheets(self):
        """Инициализация Google Sheets"""
        global sheets_manager

        sheets_manager = GoogleSheetsManager(
            credentials_path=self.credentials_path,
            spreadsheet_id=self.spreadsheet_id
        )

        await sheets_manager.initialize()
        sheets_manager.setup_sheets(self.members_sheet_name, self.activity_sheet_name)

        logger.info("✅ Google Sheets инициализирован")

    async def handle_chat_member_update(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка обновлений статуса участников канала"""
        if not update.chat_member:
            return

        chat_member_update: ChatMemberUpdated = update.chat_member
        chat = chat_member_update.chat
        new_member: ChatMember = chat_member_update.new_chat_member
        old_member: ChatMember = chat_member_update.old_chat_member

        # Проверяем, что это один из мониторенных каналов
        if chat.username not in self.monitored_channels:
            return

        logger.info(f"Обновление статуса в канале @{chat.username}: {old_member.status} -> {new_member.status}")

        # Определяем тип активности
        activity_type = self._get_activity_type(old_member, new_member)

        if activity_type:
            await self._save_member_info(chat, new_member.user, new_member.status, activity_type)
            await self._log_activity(
                new_member.user.id,
                chat.username,
                activity_type,
                old_member.status,
                new_member.status
            )

    def _get_activity_type(self, old_member: ChatMember, new_member: ChatMember) -> Optional[str]:
        """Определяет тип активности на основе изменения статуса"""
        old_status = old_member.status
        new_status = new_member.status

        if old_status in ['left', 'kicked', 'banned'] and new_status in ['member', 'administrator', 'creator']:
            return 'joined'
        elif old_status in ['member', 'administrator', 'creator'] and new_status in ['left', 'kicked', 'banned']:
            return 'left'
        elif old_status == 'member' and new_status in ['administrator', 'creator']:
            return 'promoted'
        elif old_status in ['administrator', 'creator'] and new_status == 'member':
            return 'demoted'
        elif old_status != new_status:
            return 'status_changed'

        return None

    async def _save_member_info(self, chat, user, status: str, activity_type: str):
        """Сохраняет или обновляет информацию о участнике"""
        global sheets_manager

        if not sheets_manager:
            logger.error("❌ Google Sheets менеджер не инициализирован")
            return

        if activity_type == 'joined':
            # Новый участник или повторное вступление
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
            logger.info(f"✅ Сохранен участник {user.id} ({user.username or user.first_name}) в канале @{chat.username}")

        elif activity_type == 'left':
            # Участник вышел - нужно обновить существующую запись
            # Находим участника и обновляем статус
            existing_members = sheets_manager.get_all_members(chat.username)
            for member in existing_members:
                if member.user_id == user.id:
                    member.is_active = False
                    member.left_at = datetime.utcnow()
                    sheets_manager.save_member(member)
                    logger.info(f"✅ Участник {user.id} вышел из канала @{chat.username}")
                    break

        elif activity_type in ['promoted', 'demoted', 'status_changed']:
            # Изменение статуса - обновляем существующую запись
            existing_members = sheets_manager.get_all_members(chat.username)
            for member in existing_members:
                if member.user_id == user.id:
                    member.status = status
                    sheets_manager.save_member(member)
                    logger.info(f"✅ Статус участника {user.id} изменен на {status} в канале @{chat.username}")
                    break

    async def _log_activity(self, user_id: int, channel_username: str, activity_type: str,
                          old_status: str = None, new_status: str = None):
        """Логирует активность участника"""
        global sheets_manager

        if not sheets_manager:
            logger.error("❌ Google Sheets менеджер не инициализирован")
            return

        activity = MemberActivity(
            user_id=user_id,
            channel_username=channel_username,
            activity_type=activity_type,
            old_status=old_status,
            new_status=new_status,
            timestamp=datetime.utcnow()
        )
        sheets_manager.save_activity(activity)

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /start"""
        await update.message.reply_text(
            "🤖 Бот отслеживания участников каналов запущен!\n\n"
            f"Мониторинг каналов: {', '.join(self.monitored_channels)}\n\n"
            "Доступные команды:\n"
            "/stats - статистика по каналам\n"
            "/help - справка"
        )

    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показывает статистику по каналам"""
        global sheets_manager

        if not sheets_manager:
            await update.message.reply_text("❌ Ошибка: база данных не доступна")
            return

        stats_text = "📊 Статистика по каналам:\n\n"

        for channel in self.monitored_channels:
            # Получаем статистику из Google Sheets
            stats = sheets_manager.get_channel_stats(channel)

            stats_text += f"@{channel}:\n"
            stats_text += f"  Активных: {stats['active']}\n"
            stats_text += f"  Всего: {stats['total']}\n\n"

        await update.message.reply_text(stats_text)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показывает справка"""
        help_text = """
🤖 Бот отслеживания участников Telegram каналов

Функционал:
• Автоматическое отслеживание вступлений в каналы
• Запись информации о пользователях в базу данных
• Логирование всех изменений статуса участников
• Статистика по каналам

Команды:
/start - запуск бота
/stats - показать статистику
/help - эта справка
        """
        await update.message.reply_text(help_text)

    async def run(self):
        """Запуск бота"""
        try:
            # Инициализация
            await self.init_sheets()

            # Создание приложения
            application = Application.builder().token(self.bot_token).build()

            # Добавление обработчиков
            application.add_handler(ChatMemberHandler(self.handle_chat_member_update, ChatMemberHandler.CHAT_MEMBER))
            application.add_handler(CommandHandler("start", self.start_command))
            application.add_handler(CommandHandler("stats", self.stats_command))
            application.add_handler(CommandHandler("help", self.help_command))

            logger.info("Бот запущен и готов к работе")

            # Запуск polling
            await application.run_polling()

        except Exception as e:
            logger.error(f"Ошибка при запуске бота: {e}")
            raise

async def main():
    """Главная функция"""
    try:
        bot = MemberTrackerBot()
        await bot.run()
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        raise

if __name__ == '__main__':
    asyncio.run(main())
