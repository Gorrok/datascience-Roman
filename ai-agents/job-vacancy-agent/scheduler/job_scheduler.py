"""
Планировщик задач для автоматического парсинга и отправки отчетов
"""
import asyncio
import logging
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

from config import config
from parsers import TelegramParser, detector
from ai import VacancyAnalyzer
from bot import VacancyBot

logger = logging.getLogger(__name__)


class JobScheduler:
    """Планировщик для автоматизации задач"""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.telegram_parser = TelegramParser()
        self.vacancy_analyzer = VacancyAnalyzer()
        self.vacancy_bot = VacancyBot()
    
    async def parse_channels_job(self):
        """Задача: парсинг каналов"""
        try:
            logger.info("🕐 Запуск задачи парсинга каналов...")
            
            # Парсим все каналы
            result = await self.telegram_parser.parse_all_channels(
                vacancy_detector=detector.is_vacancy
            )
            
            logger.info(
                f"✓ Парсинг завершен: {result['total_vacancies']} новых вакансий"
            )
            
            # Если найдены новые вакансии - анализируем их
            if result['total_vacancies'] > 0:
                logger.info("🤖 Начинаем анализ новых вакансий...")
                analysis_result = await self.vacancy_analyzer.analyze_all_unanalyzed()
                
                logger.info(
                    f"✓ Анализ завершен: {analysis_result['relevant']} релевантных вакансий"
                )
            
        except Exception as e:
            logger.error(f"❌ Ошибка в задаче парсинга: {e}", exc_info=True)
    
    async def send_report_job(self):
        """Задача: отправка отчета"""
        try:
            logger.info("🕐 Запуск задачи отправки отчета...")
            
            result = await self.vacancy_bot.send_vacancy_report(limit=10)
            
            logger.info(
                f"✓ Отчет отправлен: {result['sent']} вакансий"
            )
            
        except Exception as e:
            logger.error(f"❌ Ошибка в задаче отправки отчета: {e}", exc_info=True)
    
    def start(self):
        """Запустить планировщик"""
        logger.info("🚀 Запуск планировщика задач...")
        
        # Задача 1: Парсинг каналов каждые N часов
        self.scheduler.add_job(
            self.parse_channels_job,
            trigger=IntervalTrigger(hours=config.parse_interval_hours),
            id='parse_channels',
            name='Парсинг Telegram каналов',
            replace_existing=True,
            next_run_time=datetime.now()  # Запустить сразу при старте
        )
        
        logger.info(
            f"✓ Задача парсинга: каждые {config.parse_interval_hours} ч"
        )
        
        # Задача 2: Отправка отчетов раз в N дней в определенное время
        # Используем cron для более точного планирования
        self.scheduler.add_job(
            self.send_report_job,
            trigger=CronTrigger(
                day=f'*/{config.report_interval_days}',  # Каждые N дней
                hour=config.report_time_hour,
                minute=0
            ),
            id='send_report',
            name='Отправка отчета о вакансиях',
            replace_existing=True
        )
        
        logger.info(
            f"✓ Задача отчетов: каждые {config.report_interval_days} дня(ей) "
            f"в {config.report_time_hour}:00"
        )
        
        # Запускаем планировщик
        self.scheduler.start()
        logger.info("✅ Планировщик запущен")
        
        # Показываем расписание
        self.print_schedule()
    
    def stop(self):
        """Остановить планировщик"""
        self.scheduler.shutdown()
        logger.info("✓ Планировщик остановлен")
    
    def print_schedule(self):
        """Вывести расписание задач"""
        logger.info("\n📅 Расписание задач:")
        for job in self.scheduler.get_jobs():
            next_run = job.next_run_time.strftime('%Y-%m-%d %H:%M:%S') if job.next_run_time else "N/A"
            logger.info(f"  - {job.name}: следующий запуск {next_run}")
    
    async def run_once(self, task: str):
        """
        Запустить задачу один раз вручную
        
        Args:
            task: 'parse' или 'report'
        """
        if task == 'parse':
            await self.parse_channels_job()
        elif task == 'report':
            await self.send_report_job()
        else:
            logger.error(f"❌ Неизвестная задача: {task}")
