"""
Pydantic схемы для аналитики
"""
from pydantic import BaseModel
from typing import List
from datetime import datetime


class ChannelStatsResponse(BaseModel):
    total_members: int
    active_members: int
    new_today: int
    left_today: int
    inactive_members: int


class GrowthTrendItem(BaseModel):
    date: str
    joins: int
    leaves: int
    net_growth: int


class InviteLinkStatsItem(BaseModel):
    link_id: int
    link_name: str
    invite_url: str
    total_joins: int
    active_members: int
    retention_rate: float
    percentage: float


class RetentionRateResponse(BaseModel):
    period_days: int
    joined_count: int
    still_active: int
    retention_rate: float


class ActivityTimelineItem(BaseModel):
    timestamp: str
    activity_type: str
    user_id: int
    username: str | None
    first_name: str | None
    old_status: str | None
    new_status: str | None
    details: str | None
