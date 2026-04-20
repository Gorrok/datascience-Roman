"""
Pydantic схемы для подписок
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SubscriptionResponse(BaseModel):
    id: int
    user_id: int
    plan_type: str
    start_date: datetime
    end_date: Optional[datetime]
    is_active: bool
    max_bots: int
    max_channels: int
    has_sheets_export: bool
    has_api_access: bool
    history_days: int

    class Config:
        from_attributes = True


class CreateCheckoutSessionRequest(BaseModel):
    plan_type: str  # starter, professional, enterprise
    success_url: str
    cancel_url: str


class CreateCheckoutSessionResponse(BaseModel):
    session_id: str
    url: str


class CustomerPortalResponse(BaseModel):
    url: str
