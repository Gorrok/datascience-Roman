"""
Менеджер для работы с Google Sheets API.
Отвечает за сохранение и чтение данных из Google Sheets.
"""

import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from typing import List, Optional, Dict, Any
from loguru import logger

from models import ChannelMember, MemberActivity

class GoogleSheetsManager:
    """Менеджер для работы с Google Sheets"""

    # Области для аутентификации
    SCOPE = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]

    # Заголовки для таблиц
    MEMBERS_HEADERS = [
        'User ID', 'Username', 'First Name', 'Last Name',
        'Channel Username', 'Joined At', 'Left At',
        'Is Active', 'Status', 'Notes'
    ]

    ACTIVITY_HEADERS = [
        'User ID', 'Channel Username', 'Activity Type',
        'Old Status', 'New Status', 'Timestamp', 'Details'
    ]

    def __init__(self, credentials_path: str, spreadsheet_id: str):
        self.credentials_path = credentials_path
        self.spreadsheet_id = spreadsheet_id
        self.gc = None
        self.spreadsheet = None
        self.members_sheet = None
        self.activity_sheet = None

    async def initialize(self):
        """Инициализация подключения к Google Sheets"""
        try:
            logger.info("🔄 Подключаемся к Google Sheets...")

            if not os.path.exists(self.credentials_path):
                raise FileNotFoundError(f"Файл credentials.json не найден: {self.credentials_path}")

            # Авторизация
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                self.credentials_path, self.SCOPE
            )
            self.gc = gspread.authorize(creds)

            # Открываем таблицу
            self.spreadsheet = self.gc.open_by_key(self.spreadsheet_id)
            logger.info("✅ Подключение к Google Sheets установлено")

        except Exception as e:
            logger.error(f"❌ Ошибка подключения к Google Sheets: {e}")
            raise

    def setup_sheets(self, members_sheet_name: str, activity_sheet_name: str):
        """Настройка листов в таблице"""
        try:
            # Получаем или создаем листы
            try:
                self.members_sheet = self.spreadsheet.worksheet(members_sheet_name)
                logger.info(f"✅ Лист '{members_sheet_name}' найден")
            except gspread.WorksheetNotFound:
                self.members_sheet = self.spreadsheet.add_worksheet(
                    title=members_sheet_name, rows=1000, cols=10
                )
                logger.info(f"✅ Лист '{members_sheet_name}' создан")

            try:
                self.activity_sheet = self.spreadsheet.worksheet(activity_sheet_name)
                logger.info(f"✅ Лист '{activity_sheet_name}' найден")
            except gspread.WorksheetNotFound:
                self.activity_sheet = self.spreadsheet.add_worksheet(
                    title=activity_sheet_name, rows=1000, cols=7
                )
                logger.info(f"✅ Лист '{activity_sheet_name}' создан")

            # Инициализируем заголовки если они отсутствуют
            self._ensure_headers()

        except Exception as e:
            logger.error(f"❌ Ошибка настройки листов: {e}")
            raise

    def _ensure_headers(self):
        """Проверяет и устанавливает заголовки в листах"""
        try:
            # Проверяем заголовки для members
            members_data = self.members_sheet.get_all_values()
            if not members_data or len(members_data[0]) < len(self.MEMBERS_HEADERS):
                self.members_sheet.update('A1:J1', [self.MEMBERS_HEADERS])
                logger.info("✅ Заголовки для members установлены")

            # Проверяем заголовки для activity
            activity_data = self.activity_sheet.get_all_values()
            if not activity_data or len(activity_data[0]) < len(self.ACTIVITY_HEADERS):
                self.activity_sheet.update('A1:G1', [self.ACTIVITY_HEADERS])
                logger.info("✅ Заголовки для activity установлены")

        except Exception as e:
            logger.error(f"❌ Ошибка установки заголовков: {e}")

    def find_member_row(self, user_id: int, channel_username: str) -> Optional[int]:
        """Находит строку с участником в таблице"""
        try:
            # Получаем все данные
            data = self.members_sheet.get_all_values()

            # Ищем участника (пропускаем заголовок)
            for i, row in enumerate(data[1:], start=2):  # start=2 потому что enumerate от 0, а строки в sheets от 1, плюс заголовок
                if len(row) >= 5 and str(row[0]) == str(user_id) and row[4] == channel_username:
                    return i
            return None

        except Exception as e:
            logger.error(f"❌ Ошибка поиска участника: {e}")
            return None

    def save_member(self, member: ChannelMember):
        """Сохраняет или обновляет информацию об участнике"""
        try:
            row_data = member.to_row()
            row_index = self.find_member_row(member.user_id, member.channel_username)

            if row_index:
                # Обновляем существующую запись
                range_str = f'A{row_index}:J{row_index}'
                self.members_sheet.update(range_str, [row_data])
                logger.info(f"✅ Обновлен участник {member.user_id} в канале @{member.channel_username}")
            else:
                # Добавляем новую запись
                self.members_sheet.append_row(row_data)
                logger.info(f"✅ Добавлен новый участник {member.user_id} в канал @{member.channel_username}")

        except Exception as e:
            logger.error(f"❌ Ошибка сохранения участника: {e}")

    def save_activity(self, activity: MemberActivity):
        """Сохраняет запись об активности"""
        try:
            row_data = activity.to_row()
            self.activity_sheet.append_row(row_data)
            logger.info(f"✅ Сохранена активность: {activity.activity_type} для пользователя {activity.user_id}")

        except Exception as e:
            logger.error(f"❌ Ошибка сохранения активности: {e}")

    def get_channel_stats(self, channel_username: str) -> Dict[str, int]:
        """Получает статистику по каналу"""
        try:
            data = self.members_sheet.get_all_values()
            active_count = 0
            total_count = 0

            # Считаем статистику (пропускаем заголовок)
            for row in data[1:]:
                if len(row) >= 5 and row[4] == channel_username:
                    total_count += 1
                    if len(row) >= 8 and row[7].lower() == 'true':
                        active_count += 1

            return {
                'active': active_count,
                'total': total_count
            }

        except Exception as e:
            logger.error(f"❌ Ошибка получения статистики: {e}")
            return {'active': 0, 'total': 0}

    def get_all_members(self, channel_username: Optional[str] = None) -> List[ChannelMember]:
        """Получает список всех участников"""
        try:
            data = self.members_sheet.get_all_values()
            members = []

            # Преобразуем данные (пропускаем заголовок)
            for row in data[1:]:
                if len(row) >= 5:
                    if channel_username is None or row[4] == channel_username:
                        try:
                            member = ChannelMember.from_row(row)
                            members.append(member)
                        except Exception as e:
                            logger.warning(f"⚠️ Ошибка обработки строки: {e}")

            return members

        except Exception as e:
            logger.error(f"❌ Ошибка получения списка участников: {e}")
            return []

    def cleanup_inactive_members(self, days_threshold: int = 30):
        """Очищает неактивных участников старше указанного количества дней"""
        # Эта функция может быть полезна для очистки старых данных
        # Реализация зависит от требований
        pass
