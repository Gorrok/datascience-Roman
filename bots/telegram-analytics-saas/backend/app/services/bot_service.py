"""
Сервис для управления ботами
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from telegram import Bot as TelegramBot
from telegram.error import TelegramError
from loguru import logger

from app.models.bot import Bot
from app.models.user import User
from app.models.subscription import Subscription
from app.core.security import encryptor
from app.schemas.bot import BotCreate


class BotService:
    """Сервис для работы с ботами"""
    
    @staticmethod
    async def validate_bot_token(bot_token: str) -> dict:
        """Проверяет валидность токена бота через Telegram API"""
        try:
            bot = TelegramBot(token=bot_token)
            bot_info = await bot.get_me()
            
            return {
                "valid": True,
                "username": bot_info.username,
                "name": f"{bot_info.first_name}",
                "id": bot_info.id
            }
        except TelegramError as e:
            logger.error(f"Ошибка валидации токена бота: {e}")
            return {
                "valid": False,
                "error": str(e)
            }
    
    @staticmethod
    async def check_bot_limits(user: User, db: AsyncSession) -> bool:
        """Проверяет лимиты пользователя на количество ботов"""
        # Получаем подписку пользователя
        result = await db.execute(
            select(Subscription).where(Subscription.user_id == user.id)
        )
        subscription = result.scalar_one_or_none()
        
        if not subscription or not subscription.is_active:
            return False
        
        # Считаем текущее количество ботов
        result = await db.execute(
            select(Bot).where(Bot.user_id == user.id)
        )
        current_bots = len(result.scalars().all())
        
        return current_bots < subscription.max_bots
    
    @staticmethod
    async def create_bot(
        user: User,
        bot_data: BotCreate,
        db: AsyncSession
    ) -> Bot:
        """Создает нового бота"""
        
        # Валидируем токен
        validation_result = await BotService.validate_bot_token(bot_data.bot_token)
        
        if not validation_result["valid"]:
            raise ValueError(f"Невалидный токен бота: {validation_result.get('error')}")
        
        # Проверяем лимиты
        can_create = await BotService.check_bot_limits(user, db)
        if not can_create:
            raise ValueError("Достигнут лимит на количество ботов для вашего тарифа")
        
        # Шифруем токен
        encrypted_token = encryptor.encrypt(bot_data.bot_token)
        
        # Создаем бота
        new_bot = Bot(
            user_id=user.id,
            bot_token_encrypted=encrypted_token,
            bot_username=validation_result["username"],
            bot_name=validation_result["name"],
            is_active=True,
            status="stopped"
        )
        
        db.add(new_bot)
        await db.commit()
        await db.refresh(new_bot)
        
        logger.info(f"Создан новый бот {new_bot.bot_username} для пользователя {user.id}")
        
        return new_bot
    
    @staticmethod
    async def get_user_bots(user: User, db: AsyncSession) -> List[Bot]:
        """Получает всех ботов пользователя"""
        result = await db.execute(
            select(Bot).where(Bot.user_id == user.id)
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_bot_by_id(bot_id: int, user: User, db: AsyncSession) -> Optional[Bot]:
        """Получает бота по ID (только своего)"""
        result = await db.execute(
            select(Bot).where(Bot.id == bot_id, Bot.user_id == user.id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def delete_bot(bot: Bot, db: AsyncSession):
        """Удаляет бота"""
        await db.delete(bot)
        await db.commit()
        logger.info(f"Удален бот {bot.bot_username}")
    
    @staticmethod
    def decrypt_bot_token(bot: Bot) -> str:
        """Расшифровывает токен бота"""
        return encryptor.decrypt(bot.bot_token_encrypted)
