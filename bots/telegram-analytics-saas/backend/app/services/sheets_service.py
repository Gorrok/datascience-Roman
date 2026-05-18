"""
Сервис для экспорта данных в Google Sheets
Адаптирован из telegram_member_tracker/sheets_manager.py
"""
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from typing import List, Optional, Dict, Any
from loguru import logger
from sqlalchemy.orm import Session
from sqlalchemy import select
import json

from app.core.security import encryptor
from app.models.channel import Channel
from app.models.member import Member
from app.models.activity import Activity
from app.models.google_sheets_config import GoogleSheetsConfig


class GoogleSheetsService:
    """Сервис для работы с Google Sheets"""
    
    SCOPE = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    
    MEMBERS_HEADERS = [
        'User ID', 'Username', 'First Name', 'Last Name',
        'Channel ID', 'Joined At', 'Left At',
        'Is Active', 'Status', 'Notes'
    ]
    
    ACTIVITY_HEADERS = [
        'User ID', 'Channel ID', 'Activity Type',
        'Old Status', 'New Status', 'Timestamp', 'Details'
    ]
    
    def __init__(self, config: GoogleSheetsConfig, db: Session):
        self.config = config
        self.db = db
        self.gc = None
        self.spreadsheet = None
        self.members_sheet = None
        self.activity_sheet = None
    
    def initialize(self):
        """Инициализация подключения к Google Sheets"""
        try:
            logger.info("🔄 Подключаемся к Google Sheets...")
            
            # Расшифровываем credentials
            credentials_json = encryptor.decrypt(self.config.credentials_json_encrypted)
            credentials_dict = json.loads(credentials_json)
            
            # Авторизация
            creds = ServiceAccountCredentials.from_json_keyfile_dict(
                credentials_dict, self.SCOPE
            )
            self.gc = gspread.authorize(creds)
            
            # Открываем таблицу
            self.spreadsheet = self.gc.open_by_key(self.config.spreadsheet_id)
            logger.info("✅ Подключение к Google Sheets установлено")
            
            return True
        
        except Exception as e:
            logger.error(f"❌ Ошибка подключения к Google Sheets: {e}")
            return False
    
    def setup_sheets(self):
        """Настройка листов в таблице"""
        try:
            # Получаем или создаем лист Members
            try:
                self.members_sheet = self.spreadsheet.worksheet("Members")
                logger.info("✅ Лист 'Members' найден")
            except gspread.WorksheetNotFound:
                self.members_sheet = self.spreadsheet.add_worksheet(
                    title="Members", rows=1000, cols=10
                )
                logger.info("✅ Лист 'Members' создан")
            
            # Получаем или создаем лист Activity
            try:
                self.activity_sheet = self.spreadsheet.worksheet("Activity")
                logger.info("✅ Лист 'Activity' найден")
            except gspread.WorksheetNotFound:
                self.activity_sheet = self.spreadsheet.add_worksheet(
                    title="Activity", rows=1000, cols=7
                )
                logger.info("✅ Лист 'Activity' создан")
            
            # Устанавливаем заголовки
            self._ensure_headers()
            
            return True
        
        except Exception as e:
            logger.error(f"❌ Ошибка настройки листов: {e}")
            return False
    
    def _ensure_headers(self):
        """Проверяет и устанавливает заголовки в листах"""
        try:
            # Проверяем заголовки для members
            members_data = self.members_sheet.get_all_values()
            if not members_data or len(members_data[0]) < len(self.MEMBERS_HEADERS):
                self.members_sheet.update('A1:J1', [self.MEMBERS_HEADERS])
                logger.info("✅ Заголовки для Members установлены")
            
            # Проверяем заголовки для activity
            activity_data = self.activity_sheet.get_all_values()
            if not activity_data or len(activity_data[0]) < len(self.ACTIVITY_HEADERS):
                self.activity_sheet.update('A1:G1', [self.ACTIVITY_HEADERS])
                logger.info("✅ Заголовки для Activity установлены")
        
        except Exception as e:
            logger.error(f"❌ Ошибка установки заголовков: {e}")
    
    def export_members(self, channel_id: int) -> bool:
        """Экспортирует участников канала в Google Sheets"""
        try:
            # Получаем участников из БД
            members = self.db.query(Member).filter(
                Member.channel_id == channel_id
            ).all()
            
            # Очищаем лист (кроме заголовков)
            self.members_sheet.clear()
            self.members_sheet.update('A1:J1', [self.MEMBERS_HEADERS])
            
            # Формируем данные для экспорта
            rows_data = []
            for member in members:
                row = [
                    member.telegram_user_id,
                    member.username or '',
                    member.first_name or '',
                    member.last_name or '',
                    member.channel_id,
                    member.joined_at.isoformat() if member.joined_at else '',
                    member.left_at.isoformat() if member.left_at else '',
                    str(member.is_active),
                    member.status,
                    member.notes or ''
                ]
                rows_data.append(row)
            
            # Экспортируем все данные одним запросом
            if rows_data:
                self.members_sheet.append_rows(rows_data)
            
            logger.info(f"✅ Экспортировано {len(rows_data)} участников")
            return True
        
        except Exception as e:
            logger.error(f"❌ Ошибка экспорта участников: {e}")
            return False
    
    def export_activity(self, channel_id: int, limit: int = 1000) -> bool:
        """Экспортирует активность канала в Google Sheets"""
        try:
            # Получаем последние активности из БД
            activities = self.db.query(Activity).filter(
                Activity.channel_id == channel_id
            ).order_by(Activity.timestamp.desc()).limit(limit).all()
            
            # Очищаем лист (кроме заголовков)
            self.activity_sheet.clear()
            self.activity_sheet.update('A1:G1', [self.ACTIVITY_HEADERS])
            
            # Формируем данные для экспорта
            rows_data = []
            for activity in activities:
                # Получаем member для user_id
                member = self.db.query(Member).filter(
                    Member.id == activity.member_id
                ).first()
                
                if member:
                    row = [
                        member.telegram_user_id,
                        activity.channel_id,
                        activity.activity_type,
                        activity.old_status or '',
                        activity.new_status or '',
                        activity.timestamp.isoformat() if activity.timestamp else '',
                        activity.details or ''
                    ]
                    rows_data.append(row)
            
            # Экспортируем все данные одним запросом
            if rows_data:
                self.activity_sheet.append_rows(rows_data)
            
            logger.info(f"✅ Экспортировано {len(rows_data)} активностей")
            return True
        
        except Exception as e:
            logger.error(f"❌ Ошибка экспорта активности: {e}")
            return False
    
    def full_sync(self, channel_id: int) -> Dict[str, bool]:
        """Полная синхронизация данных канала"""
        results = {
            "members": False,
            "activity": False
        }
        
        if not self.initialize():
            return results
        
        if not self.setup_sheets():
            return results
        
        results["members"] = self.export_members(channel_id)
        results["activity"] = self.export_activity(channel_id)
        
        return results


def test_google_sheets_credentials(credentials_json: str, spreadsheet_id: str) -> Dict[str, Any]:
    """Тестирует подключение к Google Sheets"""
    try:
        credentials_dict = json.loads(credentials_json)
        
        creds = ServiceAccountCredentials.from_json_keyfile_dict(
            credentials_dict,
            ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        )
        gc = gspread.authorize(creds)
        
        # Пробуем открыть таблицу
        spreadsheet = gc.open_by_key(spreadsheet_id)
        
        return {
            "success": True,
            "title": spreadsheet.title,
            "message": "Подключение успешно"
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Ошибка подключения"
        }
