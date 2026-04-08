
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

TELEGRAM_BOT_TOKEN = '7773528819:AAFT2HUPl-axcFCvYVYc5uHmgQZfMNKcOfE'
CHANNEL_USERNAME = -1001589094262  # Mickey канал
SPREADSHEET_NAME = 'Invite tracker mickey'

# Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
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
async def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(ChatJoinRequestHandler(handle_join_request))

    async def run_bot():
        while True:
            await update_invite_links(app)
            await asyncio.sleep(300)

    await asyncio.gather(
        app.run_polling(),
        run_bot()
    )

if __name__ == '__main__':
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(main())
