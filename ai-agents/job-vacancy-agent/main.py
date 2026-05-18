#!/usr/bin/env python3
"""
Job Vacancy Agent - автоматический поиск вакансий через Telegram + Hermes AI

Запуск:
    python main.py                    # Запустить в фоновом режиме
    python main.py --once parse       # Разовый парсинг
    python main.py --once report      # Разовая отправка отчета
    python main.py --test             # Тестовый режим
"""
import asyncio
import sys
import logging
import argparse
from datetime import datetime
import colorlog

from config import config, validate_config
from database import init_db, close_db
from scheduler import JobScheduler
from ai import OllamaClient
from bot import VacancyBot


def setup_logging():
    """Настройка логирования с цветами"""
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    ))
    
    # Корневой логгер
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, config.log_level))
    root_logger.addHandler(handler)
    
    # Также пишем в файл
    file_handler = logging.FileHandler(config.log_file, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    root_logger.addHandler(file_handler)


async def test_mode():
    """Тестовый режим - проверка всех компонентов"""
    logger = logging.getLogger(__name__)
    
    logger.info("🧪 Запуск в тестовом режиме")
    logger.info("=" * 60)
    
    # 1. Проверка конфигурации
    logger.info("\n1️⃣ Проверка конфигурации...")
    if not validate_config():
        logger.error("❌ Конфигурация невалидна!")
        return False
    logger.info("✓ Конфигурация валидна")
    
    # 2. Проверка БД
    logger.info("\n2️⃣ Проверка базы данных...")
    try:
        await init_db()
        logger.info("✓ База данных готова")
    except Exception as e:
        logger.error(f"❌ Ошибка БД: {e}")
        return False
    
    # 3. Проверка Ollama
    logger.info("\n3️⃣ Проверка Ollama...")
    try:
        ollama_client = OllamaClient()
        if ollama_client.check_connection():
            logger.info("✓ Ollama доступен")
        else:
            logger.error("❌ Ollama недоступен")
            logger.info("Установите: curl -fsSL https://ollama.com/install.sh | sh")
            logger.info(f"Скачайте модель: ollama pull {config.ollama_model}")
            return False
    except Exception as e:
        logger.error(f"❌ Ошибка Ollama: {e}")
        return False
    
    # 4. Проверка Telegram бота
    logger.info("\n4️⃣ Проверка Telegram бота...")
    try:
        bot = VacancyBot()
        success = await bot.send_test_message()
        if success:
            logger.info("✓ Telegram бот работает, тестовое сообщение отправлено")
        else:
            logger.error("❌ Не удалось отправить тестовое сообщение")
            return False
        await bot.close()
    except Exception as e:
        logger.error(f"❌ Ошибка Telegram бота: {e}")
        return False
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ Все проверки пройдены успешно!")
    logger.info("\nСистема готова к работе. Запустите:")
    logger.info("  python main.py")
    
    return True


async def run_once(task: str):
    """Запустить задачу один раз"""
    logger = logging.getLogger(__name__)
    
    logger.info(f"🚀 Запуск задачи: {task}")
    
    # Инициализация БД
    await init_db()
    
    # Создаем scheduler
    scheduler = JobScheduler()
    
    # Запускаем задачу
    await scheduler.run_once(task)
    
    logger.info("✅ Задача выполнена")


async def run_daemon():
    """Запустить в фоновом режиме с планировщиком"""
    logger = logging.getLogger(__name__)
    
    logger.info("🚀 Запуск Job Vacancy Agent")
    logger.info("=" * 60)
    
    # Проверка конфигурации
    if not validate_config():
        logger.error("❌ Невалидная конфигурация! Выход.")
        return
    
    # Инициализация БД
    await init_db()
    
    # Проверка Ollama
    ollama_client = OllamaClient()
    if not ollama_client.check_connection():
        logger.error("❌ Ollama недоступен! Выход.")
        logger.info("Установите: curl -fsSL https://ollama.com/install.sh | sh")
        logger.info(f"Скачайте модель: ollama pull {config.ollama_model}")
        return
    
    # Отправляем уведомление о старте
    bot = VacancyBot()
    await bot.send_test_message()
    await bot.close()
    
    # Запускаем планировщик
    scheduler = JobScheduler()
    scheduler.start()
    
    logger.info("✅ Агент запущен и работает")
    logger.info("Нажмите Ctrl+C для остановки")
    
    try:
        # Бесконечный цикл
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("\n🛑 Получен сигнал остановки")
    finally:
        # Остановка планировщика
        scheduler.stop()
        
        # Закрытие БД
        await close_db()
        
        logger.info("✅ Агент остановлен")


def main():
    """Точка входа"""
    parser = argparse.ArgumentParser(
        description='Job Vacancy Agent - автоматический поиск вакансий'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Запустить в тестовом режиме (проверка всех компонентов)'
    )
    parser.add_argument(
        '--once',
        choices=['parse', 'report'],
        help='Запустить задачу один раз (parse - парсинг, report - отчет)'
    )
    
    args = parser.parse_args()
    
    # Настройка логирования
    setup_logging()
    
    # Выбор режима
    if args.test:
        success = asyncio.run(test_mode())
        sys.exit(0 if success else 1)
    elif args.once:
        asyncio.run(run_once(args.once))
    else:
        asyncio.run(run_daemon())


if __name__ == "__main__":
    main()
