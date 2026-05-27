from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from loguru import logger

from keyboards.inline import get_main_menu
from utils.api_client import APIClient

router = Router()


WELCOME_TEXT = (
    "<b>Привет, {name}!</b>\n\n"
    "Это ваш с {partner} личный планировщик.\n\n"
    "<b>Здесь можно:</b>\n"
    "• добавлять планы и хотелки\n"
    "• приглашать друг друга\n"
    "• видеть историю того, что сделали вместе\n\n"
    "Уведомления о новых планах и приглашениях будут приходить сюда автоматически.\n\n"
    "Открыть приложение — кнопка ниже или команда /app"
)


def _partner_name(message: Message) -> str:
    # Best-effort: assume there are only two users
    from bot import API_BASE_URL  # noqa: F401 -- circular-safe lazy import
    import os
    user_id = message.from_user.id
    u1 = int(os.getenv("USER_1_ID", 0))
    u2 = int(os.getenv("USER_2_ID", 0))
    n1 = os.getenv("USER_1_NAME", "партнёром")
    n2 = os.getenv("USER_2_NAME", "партнёром")
    if user_id == u1:
        return n2
    if user_id == u2:
        return n1
    return "партнёром"


@router.message(Command("start"))
async def cmd_start(message: Message, mini_app_url: str):
    partner = _partner_name(message)
    await message.answer(
        WELCOME_TEXT.format(name=message.from_user.first_name, partner=partner),
        reply_markup=get_main_menu(mini_app_url),
    )


@router.message(Command("app"))
async def cmd_app(message: Message, mini_app_url: str):
    await message.answer(
        "Открыть приложение:",
        reply_markup=get_main_menu(mini_app_url),
    )


@router.message(Command("help"))
async def cmd_help(message: Message, mini_app_url: str):
    await message.answer(
        "<b>Команды:</b>\n\n"
        "/app — открыть приложение\n"
        "/start — приветственное сообщение\n\n"
        "Всё остальное делается прямо в приложении.",
        reply_markup=get_main_menu(mini_app_url),
    )


@router.callback_query(F.data.startswith("invite_accept_"))
async def accept_invite(callback: CallbackQuery, api_client: APIClient):
    invite_id = int(callback.data.split("_")[2])
    success = await api_client.respond_to_invite(invite_id, "accepted")
    if success:
        await callback.answer("Приглашение принято")
        try:
            await callback.message.edit_text(
                f"{callback.message.text}\n\n<b>Принято</b>",
                reply_markup=None,
            )
        except Exception:
            pass
    else:
        await callback.answer("Ошибка при принятии приглашения", show_alert=True)


@router.callback_query(F.data.startswith("invite_decline_"))
async def decline_invite(callback: CallbackQuery, api_client: APIClient):
    invite_id = int(callback.data.split("_")[2])
    success = await api_client.respond_to_invite(invite_id, "declined")
    if success:
        await callback.answer("Приглашение отклонено")
        try:
            await callback.message.edit_text(
                f"{callback.message.text}\n\n<b>Отклонено</b>",
                reply_markup=None,
            )
        except Exception:
            pass
    else:
        await callback.answer("Ошибка при отклонении приглашения", show_alert=True)
