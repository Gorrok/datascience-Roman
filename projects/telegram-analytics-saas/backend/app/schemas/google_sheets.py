"""
Pydantic схемы для Google Sheets экспорта
"""
from pydantic import BaseModel
from typing import Optional


class GoogleSheetsConfigCreate(BaseModel):
    channel_id: int
    spreadsheet_id: str
    credentials_json: str  # Будет зашифрован
    auto_sync: bool = False
    sync_interval_minutes: int = 60


class GoogleSheetsConfigResponse(BaseModel):
    id: int
    user_id: int
    channel_id: int
    spreadsheet_id: str
    auto_sync: bool
    sync_interval_minutes: int

    class Config:
        from_attributes = True


class GoogleSheetsTestRequest(BaseModel):
    credentials_json: str
    spreadsheet_id: str


class GoogleSheetsTestResponse(BaseModel):
    success: bool
    title: Optional[str] = None
    message: str
    error: Optional[str] = None


class SyncResponse(BaseModel):
    success: bool
    members_synced: bool
    activity_synced: bool
    message: str
