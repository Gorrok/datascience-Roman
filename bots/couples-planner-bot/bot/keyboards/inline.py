from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo


def get_main_menu(mini_app_url: str) -> InlineKeyboardMarkup:
    """Главное меню — открыть Mini App."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Открыть приложение",
            web_app=WebAppInfo(url=mini_app_url),
        )],
    ])


def get_invite_keyboard(invite_id: int) -> InlineKeyboardMarkup:
    """Принять / отклонить инвайт."""
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✓ Принять",   callback_data=f"invite_accept_{invite_id}"),
        InlineKeyboardButton(text="✕ Отклонить", callback_data=f"invite_decline_{invite_id}"),
    ]])
