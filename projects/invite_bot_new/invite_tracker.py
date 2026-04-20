import logging
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ChatJoinRequestHandler,
    ChatMemberHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import asyncio

# Настройки — переопределяются через .env
TELEGRAM_BOT_TOKEN = 'ВАШ_ТОКЕН'
CHANNEL_USERNAME = -100XXXXXXXXXX
GROUP_ID = -100XXXXXXXXXX
SPREADSHEET_NAME = 'НазваниеТаблицы'
AUTO_APPROVE = False

# Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
links_sheet = client.open(SPREADSHEET_NAME).worksheet('Links')
members_sheet = client.open(SPREADSHEET_NAME).worksheet('Members')

processed_reactions = set()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def calc_days_diff(join_str, leave_str):
    try:
        join_dt = datetime.strptime(join_str, '%Y-%m-%d %H:%M:%S')
        leave_dt = datetime.strptime(leave_str, '%Y-%m-%d %H:%M:%S')
        return str((leave_dt - join_dt).days)
    except Exception:
        return ''


def find_user_row(user_id):
    all_values = members_sheet.get_all_values()
    for idx, row in enumerate(all_values):
        if idx == 0:
            continue
        if len(row) > 0 and str(row[0]) == str(user_id):
            return idx + 1, row
    return None, None


def ensure_user_exists(user_id, link_name='direct'):
    row_num, row_data = find_user_row(user_id)
    if row_num:
        return row_num, row_data
    join_date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    members_sheet.append_row([user_id, link_name, join_date, 'pending', '', '', '0', '0', '0'])
    logger.info(f'Создана новая запись для пользователя {user_id}')
    return find_user_row(user_id)


def set_metric(row_num, col_index, value='1'):
    try:
        current = members_sheet.cell(row_num, col_index).value
        if not current or current in ('0', ''):
            members_sheet.update_cell(row_num, col_index, value)
            return True
    except Exception as e:
        logger.error(f'Ошибка при установке метрики в колонку {col_index}: {e}')
    return False


async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Срабатывает когда пользователь отправил запрос на вступление (группа с одобрением)."""
    request = update.chat_join_request
    user = request.from_user
    invite_link = request.invite_link

    user_id = user.id
    link_name = invite_link.name if invite_link and invite_link.name else 'Без имени'
    join_date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    members_sheet.append_row([user_id, link_name, join_date, 'pending', '', '', '0', '0', '0'])
    logger.info(f'{user_id} отправил заявку по ссылке {link_name}')

    if AUTO_APPROVE:
        try:
            await request.approve()
            logger.info(f'{user_id} автоматически одобрен')
        except Exception as e:
            logger.error(f'Ошибка при авто-одобрении {user_id}: {e}')


async def handle_member_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Срабатывает при фактическом вступлении или выходе участника."""
    result = update.chat_member
    user = result.new_chat_member.user
    old_status = result.old_chat_member.status
    new_status = result.new_chat_member.status
    user_id = user.id

    is_join = new_status == 'member' and old_status in ['left', 'kicked', 'restricted']
    is_leave = old_status in ['member', 'administrator', 'creator'] and new_status in ['left', 'kicked']

    if not is_join and not is_leave:
        return

    try:
        row_num, row_data = find_user_row(user_id)

        if row_num:
            if is_join:
                members_sheet.update_cell(row_num, 4, 'subscribe')
                logger.info(f'{user_id} вступил в канал (строка {row_num})')
            elif is_leave:
                leave_date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                join_date = row_data[2] if len(row_data) > 2 else ''
                days = calc_days_diff(join_date, leave_date)
                members_sheet.update_cell(row_num, 4, 'unsubscribe')
                members_sheet.update_cell(row_num, 5, leave_date)
                members_sheet.update_cell(row_num, 6, days)
                logger.info(f'{user_id} покинул канал (был подписан {days} дней)')
        else:
            if is_join:
                join_date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                # Telegram передаёт invite_link в ChatMemberUpdated если пользователь
                # вступил по ссылке без запроса одобрения
                invite_link_obj = getattr(result, 'invite_link', None)
                link_name = 'direct'
                if invite_link_obj:
                    link_name = invite_link_obj.name or invite_link_obj.invite_link or 'direct'
                members_sheet.append_row([user_id, link_name, join_date, 'subscribe', '', '', '0', '0', '0'])
                logger.info(f'{user_id} вступил по ссылке {link_name}')

    except Exception as e:
        logger.error(f'Ошибка при обновлении статуса {user_id}: {e}')


async def handle_group_member_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Фиксирует вступление в группу (my_chat_member), колонка G."""
    try:
        result = update.my_chat_member
        if not result:
            return
        user = result.new_chat_member.user
        old_status = result.old_chat_member.status
        new_status = result.new_chat_member.status
        user_id = user.id
        is_join_group = new_status in ['member', 'administrator', 'creator'] and old_status in ['left', 'kicked', 'restricted', 'none']
        if is_join_group:
            row_num, _ = ensure_user_exists(user_id)
            if row_num and set_metric(row_num, 7, '1'):
                logger.info(f'{user_id} вступил в группу, метрика установлена')
    except Exception as e:
        logger.error(f'Ошибка при обработке вступления в группу: {e}')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Фиксирует первое сообщение участника, колонка H."""
    try:
        if not update.message or not update.message.from_user:
            return
        user_id = update.message.from_user.id
        if str(update.message.chat_id) != str(GROUP_ID):
            return
        row_num, _ = ensure_user_exists(user_id)
        if row_num and set_metric(row_num, 8, '1'):
            logger.info(f'{user_id} написал сообщение, метрика установлена')
    except Exception as e:
        logger.error(f'Ошибка при обработке сообщения: {e}')


async def handle_reaction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Фиксирует первую реакцию участника, колонка I."""
    try:
        if not update.message_reaction:
            return
        user_id = update.message_reaction.user.id if update.message_reaction.user else None
        if not user_id:
            return
        reaction_key = f"{user_id}_{update.message_reaction.message_id}"
        if reaction_key in processed_reactions:
            return
        processed_reactions.add(reaction_key)
        if len(processed_reactions) > 10000:
            processed_reactions.clear()
        row_num, _ = ensure_user_exists(user_id)
        if row_num and set_metric(row_num, 9, '1'):
            logger.info(f'{user_id} поставил реакцию, метрика установлена')
    except Exception as e:
        logger.error(f'Ошибка при обработке реакции: {e}')


async def update_invite_links(app):
    try:
        links = await app.bot.get_chat_invite_links(chat_id=CHANNEL_USERNAME)
        existing = links_sheet.col_values(2)
        for link in links:
            if link.invite_link not in existing:
                name = link.name or 'Без имени'
                date = link.create_date.strftime('%Y-%m-%d %H:%M:%S')
                links_sheet.append_row([name, link.invite_link, date])
                logger.info(f'Добавлена новая ссылка: {name} ({link.invite_link})')
    except Exception as e:
        logger.error(f'Ошибка при обновлении ссылок: {e}')


async def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(ChatJoinRequestHandler(handle_join_request))
    app.add_handler(ChatMemberHandler(handle_member_update, ChatMemberHandler.CHAT_MEMBER))
    app.add_handler(ChatMemberHandler(handle_group_member_update, ChatMemberHandler.MY_CHAT_MEMBER))
    app.add_handler(MessageHandler(filters.ALL, handle_message))

    try:
        from telegram.ext import MessageReactionHandler
        app.add_handler(MessageReactionHandler(handle_reaction))
        logger.info('Обработчик реакций добавлен')
    except ImportError:
        logger.warning('MessageReactionHandler недоступен — обновите python-telegram-bot до 20.7+')

    async def sync_links_loop():
        while True:
            await update_invite_links(app)
            await asyncio.sleep(300)

    await asyncio.gather(
        app.run_polling(allowed_updates=Update.ALL_TYPES),
        sync_links_loop()
    )


if __name__ == '__main__':
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(main())
