import logging
import time
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ChatJoinRequestHandler,
    ContextTypes,
)
import asyncio

TELEGRAM_BOT_TOKEN = '8566507218:AAEG5ifQrdlvMH3cWA5eMSRW6p7wacIAy10'
CHANNEL_USERNAME = -1001225013297  # <-- замени на ID своего канала
SPREADSHEET_NAME = 'ShepoitBukmekera'

# Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials1.json", scope)
client = gspread.authorize(creds)
links_sheet = client.open(SPREADSHEET_NAME).worksheet("Links")
members_sheet = client.open(SPREADSHEET_NAME).worksheet("Members")

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Обработка Join Request
async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = update.chat_join_request
    user = request.from_user
    invite_link = request.invite_link

    user_id = user.id
    link_name = invite_link.name or "Без имени"
    join_date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    members_sheet.append_row([user_id, link_name, join_date])
    logger.info(f"{user_id} вступил по ссылке '{link_name}'")


# Обновление списка ссылок
async def update_invite_links(app):
    try:
        links = await app.bot.get_chat_invite_links(chat_id=CHANNEL_USERNAME)
        existing = links_sheet.col_values(2)
        for link in links:
            if link.invite_link not in existing:
                name = link.name or "Без имени"
                url = link.invite_link
                date = link.create_date.strftime('%Y-%m-%d %H:%M:%S')
                links_sheet.append_row([name, url, date])
                logger.info(f"Добавлена новая ссылка: {name} ({url})")
    except Exception as e:
        logger.error(f"Ошибка при обновлении ссылок: {e}")

# Главная точка входа
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(ChatJoinRequestHandler(handle_join_request))

# Главная точка входа
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(ChatJoinRequestHandler(handle_join_request))
    
    # Добавляем job для периодического обновления ссылок
    
    app.run_polling()

if __name__ == "__main__":
    main()
