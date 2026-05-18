"""
API endpoints для экспорта в Google Sheets
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from loguru import logger

from app.core.database import get_db, SessionLocal
from app.core.security import encryptor
from app.models.user import User
from app.models.channel import Channel
from app.models.google_sheets_config import GoogleSheetsConfig
from app.api.v1.auth import get_current_user
from app.services.bot_service import BotService
from app.services.sheets_service import GoogleSheetsService, test_google_sheets_credentials
from app.schemas.google_sheets import (
    GoogleSheetsConfigCreate,
    GoogleSheetsConfigResponse,
    GoogleSheetsTestRequest,
    GoogleSheetsTestResponse,
    SyncResponse
)

router = APIRouter()


@router.post("/test", response_model=GoogleSheetsTestResponse)
async def test_connection(
    test_data: GoogleSheetsTestRequest,
    current_user: User = Depends(get_current_user)
):
    """Тестирует подключение к Google Sheets"""
    result = test_google_sheets_credentials(
        test_data.credentials_json,
        test_data.spreadsheet_id
    )
    return result


@router.post("", response_model=GoogleSheetsConfigResponse)
async def create_config(
    config_data: GoogleSheetsConfigCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Создать конфигурацию экспорта в Google Sheets"""
    
    # Проверяем доступ к каналу
    result = await db.execute(
        select(Channel).where(Channel.id == config_data.channel_id)
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
    
    # Проверяем нет ли уже конфига для этого канала
    result = await db.execute(
        select(GoogleSheetsConfig).where(
            GoogleSheetsConfig.channel_id == config_data.channel_id
        )
    )
    existing_config = result.scalar_one_or_none()
    
    if existing_config:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Конфигурация для этого канала уже существует"
        )
    
    # Шифруем credentials
    encrypted_credentials = encryptor.encrypt(config_data.credentials_json)
    
    # Создаем конфигурацию
    new_config = GoogleSheetsConfig(
        user_id=current_user.id,
        channel_id=config_data.channel_id,
        spreadsheet_id=config_data.spreadsheet_id,
        credentials_json_encrypted=encrypted_credentials,
        auto_sync=config_data.auto_sync,
        sync_interval_minutes=config_data.sync_interval_minutes
    )
    
    db.add(new_config)
    await db.commit()
    await db.refresh(new_config)
    
    return new_config


@router.get("/{channel_id}", response_model=GoogleSheetsConfigResponse)
async def get_config(
    channel_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Получить конфигурацию экспорта"""
    
    result = await db.execute(
        select(GoogleSheetsConfig).where(
            GoogleSheetsConfig.channel_id == channel_id,
            GoogleSheetsConfig.user_id == current_user.id
        )
    )
    config = result.scalar_one_or_none()
    
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Конфигурация не найдена"
        )
    
    return config


@router.post("/{channel_id}/sync", response_model=SyncResponse)
async def sync_now(
    channel_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Синхронизировать данные сейчас"""
    
    # Получаем конфигурацию
    result = await db.execute(
        select(GoogleSheetsConfig).where(
            GoogleSheetsConfig.channel_id == channel_id,
            GoogleSheetsConfig.user_id == current_user.id
        )
    )
    config = result.scalar_one_or_none()
    
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Конфигурация не найдена"
        )
    
    # Выполняем синхронизацию (используем sync session)
    try:
        sync_db = SessionLocal()
        service = GoogleSheetsService(config, sync_db)
        results = service.full_sync(channel_id)
        sync_db.close()
        
        return {
            "success": results["members"] and results["activity"],
            "members_synced": results["members"],
            "activity_synced": results["activity"],
            "message": "Синхронизация завершена"
        }
    
    except Exception as e:
        logger.error(f"Ошибка синхронизации: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка синхронизации: {str(e)}"
        )


@router.delete("/{channel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_config(
    channel_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Удалить конфигурацию экспорта"""
    
    result = await db.execute(
        select(GoogleSheetsConfig).where(
            GoogleSheetsConfig.channel_id == channel_id,
            GoogleSheetsConfig.user_id == current_user.id
        )
    )
    config = result.scalar_one_or_none()
    
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Конфигурация не найдена"
        )
    
    await db.delete(config)
    await db.commit()
    
    return None
