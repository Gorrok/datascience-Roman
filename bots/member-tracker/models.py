"""
Модели данных для работы с Google Sheets.
Здесь определены структуры данных для хранения информации о участниках каналов.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ChannelMember:
    """Модель для хранения информации о участниках каналов"""
    user_id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    channel_username: str
    joined_at: datetime
    left_at: Optional[datetime]
    is_active: bool
    status: str  # member, administrator, creator, etc.
    notes: Optional[str] = None

    @classmethod
    def from_row(cls, row: list) -> 'ChannelMember':
        """Создает объект из строки Google Sheets"""
        return cls(
            user_id=int(row[0]) if row[0] else 0,
            username=row[1] if row[1] else None,
            first_name=row[2] if row[2] else None,
            last_name=row[3] if row[3] else None,
            channel_username=row[4] if row[4] else '',
            joined_at=datetime.fromisoformat(row[5]) if row[5] else datetime.utcnow(),
            left_at=datetime.fromisoformat(row[6]) if row[6] and row[6] != 'None' else None,
            is_active=bool(row[7].lower() == 'true') if row[7] else True,
            status=row[8] if row[8] else 'member',
            notes=row[9] if len(row) > 9 and row[9] else None
        )

    def to_row(self) -> list:
        """Преобразует объект в строку для Google Sheets"""
        return [
            self.user_id,
            self.username or '',
            self.first_name or '',
            self.last_name or '',
            self.channel_username,
            self.joined_at.isoformat() if self.joined_at else '',
            self.left_at.isoformat() if self.left_at else 'None',
            str(self.is_active),
            self.status,
            self.notes or ''
        ]

@dataclass
class MemberActivity:
    """Модель для логирования активности участников"""
    user_id: int
    channel_username: str
    activity_type: str  # joined, left, promoted, etc.
    old_status: Optional[str]
    new_status: Optional[str]
    timestamp: datetime
    details: Optional[str] = None

    @classmethod
    def from_row(cls, row: list) -> 'MemberActivity':
        """Создает объект из строки Google Sheets"""
        return cls(
            user_id=int(row[0]) if row[0] else 0,
            channel_username=row[1] if row[1] else '',
            activity_type=row[2] if row[2] else '',
            old_status=row[3] if row[3] else None,
            new_status=row[4] if row[4] else None,
            timestamp=datetime.fromisoformat(row[5]) if row[5] else datetime.utcnow(),
            details=row[6] if len(row) > 6 and row[6] else None
        )

    def to_row(self) -> list:
        """Преобразует объект в строку для Google Sheets"""
        return [
            self.user_id,
            self.channel_username,
            self.activity_type,
            self.old_status or '',
            self.new_status or '',
            self.timestamp.isoformat() if self.timestamp else '',
            self.details or ''
        ]
