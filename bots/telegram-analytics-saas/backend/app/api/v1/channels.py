"""
API endpoints для управления каналами
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.models.user import User
from app.models.bot import Bot
from app.models.channel import Channel
from app.api.v1.auth import get_current_user
from app.schemas.channel import ChannelCreate, ChannelResponse, ChannelUpdate
from app.services.bot_service import BotService

router = APIRouter()


@router.post("", response_model=ChannelResponse, status_code=status.HTTP_201_CREATED)
async def create_channel(
    channel_data: ChannelCreate,
    bot_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Добавить канал для мониторинга"""
    
    # Проверяем что бот принадлежит пользователю
    bot = await BotService.get_bot_by_id(bot_id, current_user, db)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Бот не найден"
        )
    
    # Проверяем не добавлен ли уже канал
    result = await db.execute(
        select(Channel).where(
            Channel.telegram_channel_id == channel_data.telegram_channel_id
        )
    )
    existing_channel = result.scalar_one_or_none()
    
    if existing_channel:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Канал уже добавлен"
        )
    
    # Создаем канал
    new_channel = Channel(
        bot_id=bot.id,
        telegram_channel_id=channel_data.telegram_channel_id,
        channel_username=channel_data.channel_username,
        channel_title=channel_data.channel_title,
        is_monitoring=True
    )
    
    db.add(new_channel)
    await db.commit()
    await db.refresh(new_channel)
    
    return new_channel


@router.get("", response_model=List[ChannelResponse])
async def get_channels(
    bot_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Получить список каналов бота"""
    
    # Проверяем что бот принадлежит пользователю
    bot = await BotService.get_bot_by_id(bot_id, current_user, db)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Бот не найден"
        )
    
    result = await db.execute(
        select(Channel).where(Channel.bot_id == bot.id)
    )
    channels = result.scalars().all()
    
    return channels


@router.get("/{channel_id}", response_model=ChannelResponse)
async def get_channel(
    channel_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Получить информацию о канале"""
    
    result = await db.execute(
        select(Channel).where(Channel.id == channel_id)
    )
    channel = result.scalar_one_or_none()
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Канал не найден"
        )
    
    # Проверяем что канал принадлежит боту пользователя
    bot = await BotService.get_bot_by_id(channel.bot_id, current_user, db)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этому каналу"
        )
    
    return channel


@router.patch("/{channel_id}", response_model=ChannelResponse)
async def update_channel(
    channel_id: int,
    channel_data: ChannelUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Обновить настройки канала"""
    
    result = await db.execute(
        select(Channel).where(Channel.id == channel_id)
    )
    channel = result.scalar_one_or_none()
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Канал не найден"
        )
    
    # Проверяем что канал принадлежит боту пользователя
    bot = await BotService.get_bot_by_id(channel.bot_id, current_user, db)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этому каналу"
        )
    
    # Обновляем поля
    if channel_data.is_monitoring is not None:
        channel.is_monitoring = channel_data.is_monitoring
    if channel_data.channel_title is not None:
        channel.channel_title = channel_data.channel_title
    
    await db.commit()
    await db.refresh(channel)
    
    return channel


@router.delete("/{channel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_channel(
    channel_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Удалить канал"""
    
    result = await db.execute(
        select(Channel).where(Channel.id == channel_id)
    )
    channel = result.scalar_one_or_none()
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Канал не найден"
        )
    
    # Проверяем что канал принадлежит боту пользователя
    bot = await BotService.get_bot_by_id(channel.bot_id, current_user, db)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этому каналу"
        )
    
    await db.delete(channel)
    await db.commit()
    
    return None
