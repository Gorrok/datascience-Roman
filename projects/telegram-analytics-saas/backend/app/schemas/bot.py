"""
Pydantic схемы для ботов
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BotBase(BaseModel):
    bot_username: str
    bot_name: Optional[str] = None


class BotCreate(BaseModel):
    bot_token: str  # Незашифрованный токен (будет зашифрован при сохранении)


class BotUpdate(BaseModel):
    is_active: Optional[bool] = None
    bot_name: Optional[str] = None


class BotResponse(BotBase):
    id: int
    user_id: int
    created_at: datetime
    is_active: bool
    status: str
    last_error: Optional[str] = None

    class Config:
        from_attributes = True


class BotStatusUpdate(BaseModel):
    status: str  # running, stopped, error
    last_error: Optional[str] = None
