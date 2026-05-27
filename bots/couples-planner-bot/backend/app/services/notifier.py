import aiohttp
from loguru import logger
from app.core.config import settings


async def send_telegram_message(chat_id: int, text: str, reply_markup: dict | None = None) -> bool:
    """Send a message via Telegram Bot API directly from backend."""
    token = settings.TELEGRAM_BOT_TOKEN
    if not token:
        logger.warning("TELEGRAM_BOT_TOKEN not set — skipping notification")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=8)) as response:
                if response.status == 200:
                    return True
                body = await response.text()
                logger.error(f"Telegram API {response.status}: {body}")
                return False
    except Exception as e:
        logger.error(f"Failed to send Telegram message: {e}")
        return False


async def notify_invite(to_user_id: int, from_user_name: str, plan_title: str, invite_id: int) -> bool:
    """Send invite notification with accept/decline buttons."""
    text = (
        f"<b>{from_user_name}</b> приглашает вас\n\n"
        f"<i>{plan_title}</i>\n\n"
        f"Что скажете?"
    )
    keyboard = {
        "inline_keyboard": [[
            {"text": "✓ Принять",   "callback_data": f"invite_accept_{invite_id}"},
            {"text": "✕ Отклонить", "callback_data": f"invite_decline_{invite_id}"},
        ]]
    }
    return await send_telegram_message(to_user_id, text, keyboard)


async def notify_partner_about_plan(to_user_id: int, from_user_name: str, plan_title: str, plan_type: str) -> bool:
    """Notify partner that a new plan/wish was created."""
    icon = "📅" if plan_type == "plan" else "✨"
    type_label = "новый план" if plan_type == "plan" else "новое желание"
    text = (
        f"{icon} <b>{from_user_name}</b> добавил(а) {type_label}\n\n"
        f"<i>{plan_title}</i>"
    )
    return await send_telegram_message(to_user_id, text)


async def notify_invite_response(to_user_id: int, responder_name: str, plan_title: str, accepted: bool) -> bool:
    """Notify original inviter about partner's response."""
    icon = "✅" if accepted else "❌"
    verb = "приняла приглашение" if accepted else "отклонила приглашение"
    text = (
        f"{icon} <b>{responder_name}</b> {verb}\n\n"
        f"<i>{plan_title}</i>"
    )
    return await send_telegram_message(to_user_id, text)
