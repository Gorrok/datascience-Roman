"""
Парсер Telegram каналов для поиска вакансий
"""
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pyrogram import Client
from pyrogram.errors import FloodWait, ChannelPrivate, UsernameNotOccupied
import logging

from config import config
from database.models import Channel, Vacancy, ParseHistory
from database import AsyncSessionLocal
from sqlalchemy import select

logger = logging.getLogger(__name__)


class TelegramParser:
    """Парсер Telegram каналов на основе Pyrogram"""
    
    def __init__(self):
        self.client = Client(
            config.telegram_session,
            api_id=config.telegram_api_id,
            api_hash=config.telegram_api_hash,
        )
        self.is_running = False
    
    async def start(self):
        """Запустить клиент"""
        if not self.is_running:
            await self.client.start()
            self.is_running = True
            logger.info("✓ Telegram клиент запущен")
    
    async def stop(self):
        """Остановить клиент"""
        if self.is_running:
            await self.client.stop()
            self.is_running = False
            logger.info("✓ Telegram клиент остановлен")
    
    async def get_channel_messages(
        self, 
        channel_username: str, 
        limit: int = None
    ) -> List[Dict]:
        """
        Получить последние сообщения из канала
        
        Args:
            channel_username: Username канала без @
            limit: Количество сообщений (по умолчанию из config)
        
        Returns:
            Список словарей с данными сообщений
        """
        if not self.is_running:
            await self.start()
        
        if limit is None:
            limit = config.max_messages_per_channel
        
        messages_data = []
        
        try:
            logger.info(f"📥 Парсинг канала @{channel_username} (лимит: {limit})")
            
            # Получаем историю сообщений
            async for message in self.client.get_chat_history(channel_username, limit=limit):
                if message.text:
                    messages_data.append({
                        'text': message.text,
                        'message_id': message.id,
                        'date': message.date,
                        'link': f"https://t.me/{channel_username}/{message.id}",
                        'views': message.views,
                    })
            
            logger.info(f"✓ Получено {len(messages_data)} сообщений из @{channel_username}")
            
        except FloodWait as e:
            wait_seconds = e.value
            logger.warning(f"⏳ FloodWait: ожидание {wait_seconds} секунд для @{channel_username}")
            await asyncio.sleep(wait_seconds)
            # Retry
            return await self.get_channel_messages(channel_username, limit)
            
        except UsernameNotOccupied:
            logger.error(f"❌ Канал @{channel_username} не существует")
            
        except ChannelPrivate:
            logger.error(f"❌ Канал @{channel_username} приватный или недоступен")
            
        except Exception as e:
            logger.error(f"❌ Ошибка при парсинге @{channel_username}: {e}")
        
        return messages_data
    
    async def parse_channel(
        self, 
        channel_username: str,
        vacancy_detector: callable
    ) -> Dict:
        """
        Парсит канал и возвращает найденные вакансии
        
        Args:
            channel_username: Username канала
            vacancy_detector: Функция для определения является ли сообщение вакансией
        
        Returns:
            Словарь с результатами парсинга
        """
        async with AsyncSessionLocal() as session:
            # Найти или создать канал в БД
            result = await session.execute(
                select(Channel).where(Channel.username == channel_username)
            )
            channel = result.scalar_one_or_none()
            
            if not channel:
                channel = Channel(
                    username=channel_username,
                    name=channel_username,
                    active=True
                )
                session.add(channel)
                await session.commit()
                await session.refresh(channel)
            
            # Создать запись истории парсинга
            parse_record = ParseHistory(
                channel_id=channel.id,
                started_at=datetime.utcnow(),
                status='in_progress'
            )
            session.add(parse_record)
            await session.commit()
            
            try:
                # Получить сообщения
                messages = await self.get_channel_messages(channel_username)
                parse_record.messages_parsed = len(messages)
                
                vacancies_found = []
                
                # Проверить каждое сообщение
                for msg_data in messages:
                    # Проверяем что это вакансия
                    is_vacancy = vacancy_detector(msg_data['text'])
                    
                    if is_vacancy:
                        # Проверяем что такой вакансии еще нет в БД
                        existing = await session.execute(
                            select(Vacancy).where(
                                Vacancy.message_link == msg_data['link']
                            )
                        )
                        if existing.scalar_one_or_none():
                            continue  # Уже есть в БД
                        
                        # Создаем запись вакансии
                        vacancy = Vacancy(
                            channel_id=channel.id,
                            raw_text=msg_data['text'],
                            message_link=msg_data['link'],
                            posted_at=msg_data['date'],
                            found_at=datetime.utcnow(),
                        )
                        session.add(vacancy)
                        vacancies_found.append(vacancy)
                
                await session.commit()
                
                # Обновить историю парсинга
                parse_record.vacancies_found = len(vacancies_found)
                parse_record.finished_at = datetime.utcnow()
                parse_record.status = 'success'
                
                # Обновить время последней проверки канала
                channel.last_check = datetime.utcnow()
                
                await session.commit()
                
                logger.info(f"✓ Найдено {len(vacancies_found)} новых вакансий в @{channel_username}")
                
                return {
                    'channel': channel_username,
                    'messages_parsed': len(messages),
                    'vacancies_found': len(vacancies_found),
                    'status': 'success'
                }
                
            except Exception as e:
                parse_record.status = 'failed'
                parse_record.error_message = str(e)
                parse_record.finished_at = datetime.utcnow()
                await session.commit()
                
                logger.error(f"❌ Ошибка при парсинге канала @{channel_username}: {e}")
                
                return {
                    'channel': channel_username,
                    'status': 'failed',
                    'error': str(e)
                }
    
    async def parse_all_channels(self, vacancy_detector: callable) -> Dict:
        """
        Парсит все каналы из конфигурации
        
        Returns:
            Общая статистика по всем каналам
        """
        logger.info(f"🚀 Начинаем парсинг {len(config.job_channels)} каналов...")
        
        await self.start()
        
        results = []
        total_messages = 0
        total_vacancies = 0
        
        for channel in config.job_channels:
            result = await self.parse_channel(channel, vacancy_detector)
            results.append(result)
            
            if result['status'] == 'success':
                total_messages += result['messages_parsed']
                total_vacancies += result['vacancies_found']
            
            # Небольшая задержка между каналами
            await asyncio.sleep(2)
        
        await self.stop()
        
        logger.info(
            f"✅ Парсинг завершен: {total_messages} сообщений, "
            f"{total_vacancies} новых вакансий"
        )
        
        return {
            'total_channels': len(config.job_channels),
            'total_messages': total_messages,
            'total_vacancies': total_vacancies,
            'channels': results
        }
