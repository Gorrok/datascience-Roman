"""
Telegram бот для отправки отчетов о вакансиях
"""
import asyncio
import logging
from datetime import datetime
from typing import List
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import config
from database.models import Vacancy
from database import AsyncSessionLocal
from sqlalchemy import select, and_

logger = logging.getLogger(__name__)


class VacancyBot:
    """Telegram бот для отправки отчетов"""
    
    def __init__(self):
        self.bot = Bot(
            token=config.telegram_bot_token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        self.user_id = config.user_telegram_id
    
    async def send_message(self, text: str) -> bool:
        """Отправить сообщение пользователю"""
        try:
            await self.bot.send_message(
                chat_id=self.user_id,
                text=text
            )
            return True
        except Exception as e:
            logger.error(f"❌ Ошибка отправки сообщения: {e}")
            return False
    
    def format_vacancy(self, vacancy: Vacancy) -> str:
        """
        Форматирует вакансию для отправки
        
        Args:
            vacancy: Объект вакансии
        
        Returns:
            Отформатированный текст
        """
        # Заголовок
        title = vacancy.title or "Вакансия"
        text = f"<b>🎯 {title}</b>\n\n"
        
        # Компания
        if vacancy.company:
            text += f"🏢 <b>Компания:</b> {vacancy.company}\n"
        
        # Зарплата
        if vacancy.salary and vacancy.salary != "--":
            text += f"💰 <b>Зарплата:</b> {vacancy.salary}\n"
        
        # Локация и режим
        location_parts = []
        if vacancy.location:
            location_parts.append(vacancy.location)
        if vacancy.work_mode:
            location_parts.append(vacancy.work_mode)
        if location_parts:
            text += f"📍 <b>Локация:</b> {', '.join(location_parts)}\n"
        
        # Описание
        if vacancy.description:
            text += f"\n📝 {vacancy.description}\n"
        
        # Релевантность
        score_percent = int(vacancy.relevance_score * 100)
        text += f"\n⭐️ <b>Релевантность:</b> {score_percent}%\n"
        
        # Причины совпадения
        if vacancy.match_reason:
            reasons = vacancy.match_reason.split('\n')
            positive_reasons = [r for r in reasons if r.startswith('✓')]
            if positive_reasons:
                text += f"\n<b>Подходит потому что:</b>\n"
                for reason in positive_reasons[:3]:  # Топ-3
                    text += f"  {reason}\n"
        
        # Канал
        if vacancy.channel:
            text += f"\n📢 <b>Канал:</b> @{vacancy.channel.username}\n"
        
        # Ссылка
        if vacancy.message_link:
            text += f"\n🔗 <a href='{vacancy.message_link}'>Открыть в Telegram</a>\n"
        
        # Разделитель
        text += "\n" + "─" * 40
        
        return text
    
    async def send_vacancy_report(self, limit: int = 10) -> Dict:
        """
        Отправляет отчет с новыми релевантными вакансиями
        
        Args:
            limit: Максимум вакансий в отчете
        
        Returns:
            Статистика отправки
        """
        logger.info("📨 Подготовка отчета о вакансиях...")
        
        async with AsyncSessionLocal() as session:
            # Найти релевантные вакансии которые еще не были отправлены
            result = await session.execute(
                select(Vacancy)
                .where(
                    and_(
                        Vacancy.is_relevant == True,
                        Vacancy.sent_to_user == False
                    )
                )
                .order_by(Vacancy.relevance_score.desc())
                .limit(limit)
            )
            vacancies = result.scalars().all()
        
        if not vacancies:
            logger.info("ℹ️ Нет новых релевантных вакансий для отправки")
            
            # Отправим уведомление что нет вакансий
            await self.send_message(
                "🔍 <b>Отчет о вакансиях</b>\n\n"
                "На данный момент новых релевантных вакансий не найдено.\n"
                "Продолжаю мониторинг каналов. 🚀"
            )
            
            return {
                'total': 0,
                'sent': 0,
                'failed': 0
            }
        
        logger.info(f"📊 Найдено {len(vacancies)} новых релевантных вакансий")
        
        # Отправляем заголовок отчета
        header = (
            f"🎯 <b>Отчет о вакансиях</b>\n"
            f"📅 {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
            f"Найдено <b>{len(vacancies)}</b> подходящих вакансий:\n\n"
        )
        await self.send_message(header)
        
        sent = 0
        failed = 0
        
        # Отправляем каждую вакансию
        for i, vacancy in enumerate(vacancies, 1):
            try:
                text = self.format_vacancy(vacancy)
                success = await self.send_message(text)
                
                if success:
                    sent += 1
                    
                    # Отмечаем как отправленную
                    async with AsyncSessionLocal() as session:
                        result = await session.execute(
                            select(Vacancy).where(Vacancy.id == vacancy.id)
                        )
                        db_vacancy = result.scalar_one()
                        db_vacancy.sent_to_user = True
                        db_vacancy.sent_at = datetime.utcnow()
                        await session.commit()
                    
                    logger.info(f"✓ Отправлена вакансия {i}/{len(vacancies)}: {vacancy.title}")
                else:
                    failed += 1
                
                # Задержка между сообщениями чтобы не словить flood
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"❌ Ошибка отправки вакансии ID {vacancy.id}: {e}")
                failed += 1
        
        # Футер отчета
        footer = (
            f"\n✅ <b>Отчет завершен</b>\n"
            f"Отправлено: {sent} вакансий\n"
            f"Следующий отчет через {config.report_interval_days} дня(ей)"
        )
        await self.send_message(footer)
        
        logger.info(f"✅ Отчет отправлен: {sent} успешно, {failed} ошибок")
        
        return {
            'total': len(vacancies),
            'sent': sent,
            'failed': failed
        }
    
    async def send_test_message(self) -> bool:
        """Отправить тестовое сообщение"""
        text = (
            "🤖 <b>Job Vacancy Agent</b>\n\n"
            "Бот успешно запущен и готов к работе!\n"
            "Буду отправлять отчеты о подходящих вакансиях "
            f"каждые {config.report_interval_days} дня(ей)."
        )
        return await self.send_message(text)
    
    async def close(self):
        """Закрыть соединение с ботом"""
        await self.bot.session.close()
        logger.info("✓ Telegram бот закрыт")
