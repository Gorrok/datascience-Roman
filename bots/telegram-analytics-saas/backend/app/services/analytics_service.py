"""
Сервис аналитики для расчета метрик каналов
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from datetime import datetime, timedelta
from typing import Dict, List, Any

from app.models.channel import Channel
from app.models.member import Member
from app.models.activity import Activity
from app.models.invite_link import InviteLink


class AnalyticsService:
    """Сервис для расчета аналитических метрик"""
    
    @staticmethod
    async def get_channel_stats(channel_id: int, db: AsyncSession) -> Dict[str, Any]:
        """Получает основную статистику канала"""
        
        # Всего участников
        result = await db.execute(
            select(func.count(Member.id)).where(Member.channel_id == channel_id)
        )
        total_members = result.scalar() or 0
        
        # Активные участники
        result = await db.execute(
            select(func.count(Member.id)).where(
                and_(
                    Member.channel_id == channel_id,
                    Member.is_active == True
                )
            )
        )
        active_members = result.scalar() or 0
        
        # Новые участники сегодня
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        result = await db.execute(
            select(func.count(Member.id)).where(
                and_(
                    Member.channel_id == channel_id,
                    Member.joined_at >= today_start
                )
            )
        )
        new_today = result.scalar() or 0
        
        # Вышедшие сегодня
        result = await db.execute(
            select(func.count(Member.id)).where(
                and_(
                    Member.channel_id == channel_id,
                    Member.left_at >= today_start,
                    Member.is_active == False
                )
            )
        )
        left_today = result.scalar() or 0
        
        return {
            "total_members": total_members,
            "active_members": active_members,
            "new_today": new_today,
            "left_today": left_today,
            "inactive_members": total_members - active_members
        }
    
    @staticmethod
    async def get_growth_trend(
        channel_id: int,
        days: int,
        db: AsyncSession
    ) -> List[Dict[str, Any]]:
        """Получает тренд роста за последние N дней"""
        
        trend_data = []
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        for i in range(days):
            day_start = today - timedelta(days=i)
            day_end = day_start + timedelta(days=1)
            
            # Вступления за день
            result = await db.execute(
                select(func.count(Member.id)).where(
                    and_(
                        Member.channel_id == channel_id,
                        Member.joined_at >= day_start,
                        Member.joined_at < day_end
                    )
                )
            )
            joins = result.scalar() or 0
            
            # Выходы за день
            result = await db.execute(
                select(func.count(Member.id)).where(
                    and_(
                        Member.channel_id == channel_id,
                        Member.left_at >= day_start,
                        Member.left_at < day_end
                    )
                )
            )
            leaves = result.scalar() or 0
            
            trend_data.append({
                "date": day_start.isoformat(),
                "joins": joins,
                "leaves": leaves,
                "net_growth": joins - leaves
            })
        
        return list(reversed(trend_data))
    
    @staticmethod
    async def get_invite_links_stats(
        channel_id: int,
        db: AsyncSession
    ) -> List[Dict[str, Any]]:
        """Получает статистику по инвайт-ссылкам"""
        
        # Получаем все инвайт-ссылки канала
        result = await db.execute(
            select(InviteLink).where(InviteLink.channel_id == channel_id)
        )
        invite_links = result.scalars().all()
        
        stats = []
        total_joins = 0
        
        for link in invite_links:
            # Считаем участников по ссылке
            result = await db.execute(
                select(func.count(Member.id)).where(
                    Member.invite_link_id == link.id
                )
            )
            joins_count = result.scalar() or 0
            total_joins += joins_count
            
            # Активных участников по ссылке
            result = await db.execute(
                select(func.count(Member.id)).where(
                    and_(
                        Member.invite_link_id == link.id,
                        Member.is_active == True
                    )
                )
            )
            active_count = result.scalar() or 0
            
            stats.append({
                "link_id": link.id,
                "link_name": link.link_name,
                "invite_url": link.invite_url,
                "total_joins": joins_count,
                "active_members": active_count,
                "retention_rate": round((active_count / joins_count * 100) if joins_count > 0 else 0, 2)
            })
        
        # Сортируем по количеству вступлений
        stats.sort(key=lambda x: x["total_joins"], reverse=True)
        
        # Добавляем процент от общего
        for stat in stats:
            stat["percentage"] = round((stat["total_joins"] / total_joins * 100) if total_joins > 0 else 0, 2)
        
        return stats
    
    @staticmethod
    async def get_retention_rate(
        channel_id: int,
        days: int,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Рассчитывает retention rate (процент оставшихся участников)"""
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Участники присоединившиеся N дней назад
        result = await db.execute(
            select(func.count(Member.id)).where(
                and_(
                    Member.channel_id == channel_id,
                    Member.joined_at <= cutoff_date
                )
            )
        )
        joined_before = result.scalar() or 0
        
        # Из них все еще активны
        result = await db.execute(
            select(func.count(Member.id)).where(
                and_(
                    Member.channel_id == channel_id,
                    Member.joined_at <= cutoff_date,
                    Member.is_active == True
                )
            )
        )
        still_active = result.scalar() or 0
        
        retention = round((still_active / joined_before * 100) if joined_before > 0 else 0, 2)
        
        return {
            "period_days": days,
            "joined_count": joined_before,
            "still_active": still_active,
            "retention_rate": retention
        }
    
    @staticmethod
    async def get_activity_timeline(
        channel_id: int,
        limit: int,
        db: AsyncSession
    ) -> List[Dict[str, Any]]:
        """Получает последние события активности"""
        
        result = await db.execute(
            select(Activity, Member)
            .join(Member, Activity.member_id == Member.id)
            .where(Activity.channel_id == channel_id)
            .order_by(Activity.timestamp.desc())
            .limit(limit)
        )
        
        timeline = []
        for activity, member in result:
            timeline.append({
                "timestamp": activity.timestamp.isoformat(),
                "activity_type": activity.activity_type,
                "user_id": member.telegram_user_id,
                "username": member.username,
                "first_name": member.first_name,
                "old_status": activity.old_status,
                "new_status": activity.new_status,
                "details": activity.details
            })
        
        return timeline
