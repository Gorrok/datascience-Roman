import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = "YOUR_BOT_TOKEN"
TARGET_CHAT_ID = None  # None = реагирует в любой группе, или укажи конкретный chat_id: -1001234567890

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return

    if TARGET_CHAT_ID and message.chat_id != TARGET_CHAT_ID:
        return

    if 'онлайн' in message.text.lower():
        logger.info(f"Слово 'онлайн' найдено в чате {message.chat_id}, сообщение от {message.from_user.username}")
        await message.reply_text(
            "не забудь включить Mymeat 🎥",
            reply_to_message_id=message.message_id
        )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("Бот запущен. Жду слово 'онлайн'...")
    app.run_polling()

if __name__ == '__main__':
    main()
