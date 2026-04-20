import asyncio
import os
from dotenv import load_dotenv
from loguru import logger

# Загрузка переменных окружения
load_dotenv()

def test_configuration():
    """Проверка конфигурации бота"""
    logger.info("🔍 Проверка конфигурации бота...")

    # Проверка токена бота
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        logger.error("❌ TELEGRAM_BOT_TOKEN не найден в .env файле")
        return False
    else:
        logger.info("✅ TELEGRAM_BOT_TOKEN найден")

    # Проверка каналов для мониторинга
    monitored_channels = os.getenv('MONITORED_CHANNELS', '')
    if not monitored_channels:
        logger.warning("⚠️  MONITORED_CHANNELS не указаны. Добавьте каналы в .env")
    else:
        channels = [ch.strip() for ch in monitored_channels.split(',') if ch.strip()]
        logger.info(f"✅ Мониторинг каналов: {channels}")

    # Проверка URL базы данных
    db_url = os.getenv('DATABASE_URL', 'sqlite:///member_tracker.db')
    logger.info(f"✅ База данных: {db_url}")

    # Проверка директории логов
    log_file = os.getenv('LOG_FILE', 'logs/bot.log')
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
        logger.info(f"✅ Создана директория для логов: {log_dir}")
    else:
        logger.info("✅ Директория для логов существует")

    return True

async def test_google_sheets_connection():
    """Проверка подключения к Google Sheets"""
    try:
        from sheets_manager import GoogleSheetsManager

        credentials_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH', 'credentials.json')
        spreadsheet_id = os.getenv('GOOGLE_SHEETS_SPREADSHEET_ID')

        if not spreadsheet_id:
            logger.error("❌ GOOGLE_SHEETS_SPREADSHEET_ID не найден в .env файле")
            return False

        if not os.path.exists(credentials_path):
            logger.error(f"❌ Файл {credentials_path} не найден")
            return False

        sheets_manager = GoogleSheetsManager(
            credentials_path=credentials_path,
            spreadsheet_id=spreadsheet_id
        )

        await sheets_manager.initialize()
        logger.info("✅ Подключение к Google Sheets успешно")
        return True

    except Exception as e:
        logger.error(f"❌ Ошибка подключения к Google Sheets: {e}")
        return False

async def test_bot_token():
    """Проверка токена бота"""
    try:
        from telegram import Bot

        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not bot_token:
            return False

        bot = Bot(token=bot_token)
        bot_info = await bot.get_me()

        logger.info(f"✅ Бот подключен: @{bot_info.username} (ID: {bot_info.id})")
        return True

    except Exception as e:
        logger.error(f"❌ Ошибка проверки токена бота: {e}")
        return False

async def run_tests():
    """Запуск всех тестов"""
    logger.info("🚀 Запуск тестирования бота...")

    tests = [
        ("Конфигурация", test_configuration()),
        ("Google Sheets", await test_google_sheets_connection()),
        ("Токен бота", await test_bot_token()),
    ]

    passed = 0
    total = len(tests)

    logger.info("\n" + "="*50)
    logger.info("📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
    logger.info("="*50)

    for test_name, result in tests:
        status = "✅ ПРОЙДЕН" if result else "❌ ПРОВАЛЕН"
        logger.info(f"{test_name}: {status}")
        if result:
            passed += 1

    logger.info("="*50)
    logger.info(f"ИТОГО: {passed}/{total} тестов пройдено")

    if passed == total:
        logger.info("🎉 Все тесты пройдены! Бот готов к запуску.")
        logger.info("Запустите бота командой: python bot.py")
    else:
        logger.error("⚠️  Некоторые тесты провалены. Исправьте ошибки перед запуском.")

    return passed == total

if __name__ == '__main__':
    asyncio.run(run_tests())
