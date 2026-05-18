"""
Pydantic схемы для каналов
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ChannelBase(BaseModel):
    channel_username: Optional[str] = None
    channel_title: Optional[str] = None


class ChannelCreate(BaseModel):
    telegram_channel_id: int
    channel_username: Optional[str] = None
    channel_title: Optional[str] = None


class ChannelUpdate(BaseModel):
    is_monitoring: Optional[bool] = None
    channel_title: Optional[str] = None


class ChannelResponse(ChannelBase):
    id: int
    bot_id: int
    telegram_channel_id: int
    added_at: datetime
    is_monitoring: bool

    class Config:
        from_attributes = True


class ChannelStats(BaseModel):
    total_members: int
    active_members: int
    new_members_today: int
    left_members_today: int
