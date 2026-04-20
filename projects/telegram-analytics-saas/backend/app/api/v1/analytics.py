"""
API endpoints для аналитики
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.models.user import User
from app.models.channel import Channel
from app.api.v1.auth import get_current_user
from app.services.bot_service import BotService
from app.services.analytics_service import AnalyticsService
from app.schemas.analytics import (
    ChannelStatsResponse,
    GrowthTrendItem,
    InviteLinkStatsItem,
    RetentionRateResponse,
    ActivityTimelineItem
)

router = APIRouter()


@router.get("/channels/{channel_id}/stats", response_model=ChannelStatsResponse)
async def get_channel_stats(
    channel_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Получить основную статистику канала"""
    
    # Проверяем доступ к каналу
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
    
    stats = await AnalyticsService.get_channel_stats(channel_id, db)
    return stats


@router.get("/channels/{channel_id}/growth-trend", response_model=List[GrowthTrendItem])
async def get_growth_trend(
    channel_id: int,
    days: int = Query(default=30, ge=1, le=365),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Получить тренд роста канала за последние N дней"""
    
    # Проверяем доступ к каналу
    result = await db.execute(
        select(Channel).where(Channel.id == channel_id)
    )
    channel = result.scalar_one_or_none()
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Канал не найден"
        )
    
    bot = await BotService.get_bot_by_id(channel.bot_id, current_user, db)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этому каналу"
        )
    
    trend = await AnalyticsService.get_growth_trend(channel_id, days, db)
    return trend


@router.get("/channels/{channel_id}/invite-links", response_model=List[InviteLinkStatsItem])
async def get_invite_links_stats(
    channel_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Получить статистику по инвайт-ссылкам"""
    
    # Проверяем доступ к каналу
    result = await db.execute(
        select(Channel).where(Channel.id == channel_id)
    )
    channel = result.scalar_one_or_none()
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Канал не найден"
        )
    
    bot = await BotService.get_bot_by_id(channel.bot_id, current_user, db)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этому каналу"
        )
    
    stats = await AnalyticsService.get_invite_links_stats(channel_id, db)
    return stats


@router.get("/channels/{channel_id}/retention", response_model=RetentionRateResponse)
async def get_retention_rate(
    channel_id: int,
    days: int = Query(default=30, ge=1, le=365),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Получить retention rate (процент оставшихся участников)"""
    
    # Проверяем доступ к каналу
    result = await db.execute(
        select(Channel).where(Channel.id == channel_id)
    )
    channel = result.scalar_one_or_none()
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Канал не найден"
        )
    
    bot = await BotService.get_bot_by_id(channel.bot_id, current_user, db)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этому каналу"
        )
    
    retention = await AnalyticsService.get_retention_rate(channel_id, days, db)
    return retention


@router.get("/channels/{channel_id}/activity", response_model=List[ActivityTimelineItem])
async def get_activity_timeline(
    channel_id: int,
    limit: int = Query(default=50, ge=1, le=200),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Получить timeline активности канала"""
    
    # Проверяем доступ к каналу
    result = await db.execute(
        select(Channel).where(Channel.id == channel_id)
    )
    channel = result.scalar_one_or_none()
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Канал не найден"
        )
    
    bot = await BotService.get_bot_by_id(channel.bot_id, current_user, db)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этому каналу"
        )
    
    timeline = await AnalyticsService.get_activity_timeline(channel_id, limit, db)
    return timeline
