"""
API endpoints для управления ботами
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.models.user import User
from app.models.bot import Bot
from app.api.v1.auth import get_current_user
from app.schemas.bot import BotCreate, BotResponse, BotStatusUpdate
from app.services.bot_service import BotService
from app.tasks.bot_polling import start_bot_task, stop_bot_task

router = APIRouter()


@router.post("", response_model=BotResponse, status_code=status.HTTP_201_CREATED)
async def create_bot(
    bot_data: BotCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Создать нового бота"""
    try:
        bot = await BotService.create_bot(current_user, bot_data, db)
        return bot
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("", response_model=List[BotResponse])
async def get_bots(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Получить список всех ботов пользователя"""
    bots = await BotService.get_user_bots(current_user, db)
    return bots


@router.get("/{bot_id}", response_model=BotResponse)
async def get_bot(
    bot_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Получить информацию о боте"""
    bot = await BotService.get_bot_by_id(bot_id, current_user, db)
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Бот не найден"
        )
    
    return bot


@router.post("/{bot_id}/start")
async def start_bot(
    bot_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Запустить бота"""
    bot = await BotService.get_bot_by_id(bot_id, current_user, db)
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Бот не найден"
        )
    
    if bot.status == "running":
        return {"message": "Бот уже запущен", "status": "running"}
    
    # Запускаем Celery задачу для бота
    try:
        start_bot_task.delay(bot_id)
        
        bot.status = "running"
        bot.last_error = None
        await db.commit()
        
        return {"message": "Бот запущен", "status": "running"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка запуска бота: {str(e)}"
        )


@router.post("/{bot_id}/stop")
async def stop_bot(
    bot_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Остановить бота"""
    bot = await BotService.get_bot_by_id(bot_id, current_user, db)
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Бот не найден"
        )
    
    if bot.status == "stopped":
        return {"message": "Бот уже остановлен", "status": "stopped"}
    
    # Останавливаем Celery задачу
    try:
        stop_bot_task.delay(bot_id)
        
        bot.status = "stopped"
        await db.commit()
        
        return {"message": "Бот остановлен", "status": "stopped"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка остановки бота: {str(e)}"
        )


@router.delete("/{bot_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bot(
    bot_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Удалить бота"""
    bot = await BotService.get_bot_by_id(bot_id, current_user, db)
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Бот не найден"
        )
    
    # Останавливаем бота если он запущен
    if bot.status == "running":
        stop_bot_task.delay(bot_id)
    
    await BotService.delete_bot(bot, db)
    
    return None
