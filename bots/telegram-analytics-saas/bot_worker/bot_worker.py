"""
Bot Worker - адаптированный из telegram_member_tracker/bot.py
Работает с PostgreSQL вместо Google Sheets и интегрирован с Celery
"""
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
from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import encryptor
from app.models.bot import Bot
from app.models.channel import Channel
from app.models.member import Member
from app.models.activity import Activity
from app.models.invite_link import InviteLink


class TelegramBotWorker:
    """Воркер для мониторинга Telegram канала"""
    
    def __init__(self, bot_id: int):
        self.bot_id = bot_id
        self.db = SessionLocal()
        self.bot_token = None
        self.monitored_channels = []
        self.application = None
        
        # Загружаем данные бота
        self._load_bot_data()
    
    def _load_bot_data(self):
        """Загружает данные бота из БД"""
        bot = self.db.query(Bot).filter(Bot.id == self.bot_id).first()
        
        if not bot:
            raise ValueError(f"Бот с ID {self.bot_id} не найден")
        
        # Расшифровываем токен
        self.bot_token = encryptor.decrypt(bot.bot_token_encrypted)
        
        # Получаем каналы для мониторинга
        channels = self.db.query(Channel).filter(
            Channel.bot_id == self.bot_id,
            Channel.is_monitoring == True
        ).all()
        
        self.monitored_channels = [ch.telegram_channel_id for ch in channels]
        
        logger.info(f"Загружен бот {bot.bot_username}, каналов для мониторинга: {len(self.monitored_channels)}")
    
    async def handle_chat_member_update(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка обновлений статуса участников канала"""
        if not update.chat_member:
            return
        
        chat_member_update: ChatMemberUpdated = update.chat_member
        chat = chat_member_update.chat
        new_member: ChatMember = chat_member_update.new_chat_member
        old_member: ChatMember = chat_member_update.old_chat_member
        
        # Проверяем, что это один из мониторенных каналов
        if chat.id not in self.monitored_channels:
            return
        
        logger.info(f"Обновление статуса в канале {chat.id}: {old_member.status} -> {new_member.status}")
        
        # Определяем тип активности
        activity_type = self._get_activity_type(old_member, new_member)
        
        if activity_type:
            await self._save_member_info(chat, new_member.user, new_member.status, activity_type)
    
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
        try:
            # Получаем канал
            channel = self.db.query(Channel).filter(
                Channel.telegram_channel_id == chat.id
            ).first()
            
            if not channel:
                logger.error(f"Канал {chat.id} не найден в БД")
                return
            
            if activity_type == 'joined':
                # Проверяем существует ли участник
                existing_member = self.db.query(Member).filter(
                    Member.channel_id == channel.id,
                    Member.telegram_user_id == user.id
                ).first()
                
                if existing_member:
                    # Обновляем существующего
                    existing_member.is_active = True
                    existing_member.left_at = None
                    existing_member.status = status
                    existing_member.username = user.username
                    existing_member.first_name = user.first_name
                    existing_member.last_name = user.last_name
                else:
                    # Создаем нового
                    new_member = Member(
                        channel_id=channel.id,
                        telegram_user_id=user.id,
                        username=user.username,
                        first_name=user.first_name,
                        last_name=user.last_name,
                        joined_at=datetime.utcnow(),
                        is_active=True,
                        status=status
                    )
                    self.db.add(new_member)
                
                logger.info(f"✅ Сохранен участник {user.id} в канале {chat.id}")
            
            elif activity_type == 'left':
                # Находим участника и обновляем
                member = self.db.query(Member).filter(
                    Member.channel_id == channel.id,
                    Member.telegram_user_id == user.id
                ).first()
                
                if member:
                    member.is_active = False
                    member.left_at = datetime.utcnow()
                    member.status = status
                    logger.info(f"✅ Участник {user.id} вышел из канала {chat.id}")
            
            # Логируем активность
            await self._log_activity(user.id, channel.id, activity_type, status)
            
            self.db.commit()
        
        except Exception as e:
            logger.error(f"❌ Ошибка сохранения участника: {e}")
            self.db.rollback()
    
    async def _log_activity(self, user_id: int, channel_id: int, activity_type: str, status: str):
        """Логирует активность участника"""
        try:
            # Находим member_id
            member = self.db.query(Member).filter(
                Member.channel_id == channel_id,
                Member.telegram_user_id == user_id
            ).first()
            
            if not member:
                return
            
            activity = Activity(
                member_id=member.id,
                channel_id=channel_id,
                activity_type=activity_type,
                new_status=status,
                timestamp=datetime.utcnow()
            )
            self.db.add(activity)
        
        except Exception as e:
            logger.error(f"❌ Ошибка логирования активности: {e}")
    
    async def run(self):
        """Запускает бота"""
        try:
            logger.info(f"🚀 Запуск бота {self.bot_id}")
            
            # Создаем приложение
            self.application = Application.builder().token(self.bot_token).build()
            
            # Добавляем обработчик обновлений статуса участников
            self.application.add_handler(
                ChatMemberHandler(self.handle_chat_member_update, ChatMemberHandler.CHAT_MEMBER)
            )
            
            logger.info("Бот запущен и готов к работе")
            
            # Запуск polling
            await self.application.run_polling()
        
        except Exception as e:
            logger.error(f"Ошибка при запуске бота: {e}")
            
            # Обновляем статус бота в БД
            bot = self.db.query(Bot).filter(Bot.id == self.bot_id).first()
            if bot:
                bot.status = "error"
                bot.last_error = str(e)
                self.db.commit()
            
            raise
        finally:
            self.db.close()
    
    async def stop(self):
        """Останавливает бота"""
        if self.application:
            await self.application.stop()
            logger.info(f"🛑 Бот {self.bot_id} остановлен")


async def run_bot_worker(bot_id: int):
    """Запускает bot worker"""
    worker = TelegramBotWorker(bot_id)
    await worker.run()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python bot_worker.py <bot_id>")
        sys.exit(1)
    
    bot_id = int(sys.argv[1])
    asyncio.run(run_bot_worker(bot_id))
