import asyncio
import os
import sys
from dotenv import load_dotenv
from loguru import logger

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand

from handlers import main
from utils.api_client import APIClient

load_dotenv()

# Настройка логирования
logger.add(
    "logs/bot.log",
    rotation="1 day",
    retention="7 days",
    level="INFO"
)

# Конфигурация
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_HOST = os.getenv("API_HOST", "localhost")
API_PORT = os.getenv("API_PORT", "8000")
MINI_APP_URL = os.getenv("MINI_APP_URL", "https://your-domain.com")

if not TELEGRAM_BOT_TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
    sys.exit(1)

API_BASE_URL = f"http://{API_HOST}:{API_PORT}"

async def send_invite_notification(
    bot: Bot,
    to_user_id: int,
    from_user_name: str,
    plan_title: str,
    invite_id: int
):
    """Отправить уведомление о новом инвайте"""
    from keyboards.inline import get_invite_keyboard
    
    try:
        await bot.send_message(
            to_user_id,
            f"💌 {from_user_name} пригласил(а) вас на:\n\n"
            f"📝 {plan_title}\n\n"
            f"Примете приглашение?",
            reply_markup=get_invite_keyboard(invite_id)
        )
    except Exception as e:
        logger.error(f"Failed to send invite notification: {e}")

async def main_bot():
    bot = Bot(
        token=TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    
    # Инициализируем API клиент
    api_client = APIClient(API_BASE_URL)
    await api_client.init_session()
    
    # Регистрируем роутеры
    dp.include_router(main.router)
    
    # Добавляем зависимости в контекст
    dp["api_client"] = api_client
    dp["mini_app_url"] = MINI_APP_URL
    
    # Middleware для инъекции зависимостей
    @dp.update.outer_middleware()
    async def inject_dependencies(handler, event, data):
        data["api_client"] = api_client
        data["mini_app_url"] = MINI_APP_URL
        return await handler(event, data)
    
    await bot.set_my_commands([
        BotCommand(command="app",   description="Открыть приложение"),
        BotCommand(command="start", description="Приветствие"),
        BotCommand(command="help",  description="Помощь"),
    ])

    logger.info("Starting bot...")

    try:
        await dp.start_polling(bot)
    finally:
        await api_client.close_session()
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main_bot())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
