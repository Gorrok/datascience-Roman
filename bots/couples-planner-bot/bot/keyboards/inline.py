from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

def get_main_menu(mini_app_url: str) -> InlineKeyboardMarkup:
    """Главное меню с кнопкой открытия Mini App"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🎯 Открыть планировщик",
                web_app=WebAppInfo(url=mini_app_url)
            )
        ],
        [
            InlineKeyboardButton(
                text="📋 Мои планы",
                callback_data="my_plans"
            )
        ],
        [
            InlineKeyboardButton(
                text="📨 Инвайты",
                callback_data="my_invites"
            )
        ]
    ])
    return keyboard

def get_invite_keyboard(invite_id: int) -> InlineKeyboardMarkup:
    """Клавиатура для ответа на инвайт"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ Принять",
                callback_data=f"invite_accept_{invite_id}"
            ),
            InlineKeyboardButton(
                text="❌ Отклонить",
                callback_data=f"invite_decline_{invite_id}"
            )
        ]
    ])
    return keyboard

def get_plan_keyboard(plan_id: int) -> InlineKeyboardMarkup:
    """Клавиатура для действий с планом"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ Выполнено",
                callback_data=f"plan_complete_{plan_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔙 Назад",
                callback_data="my_plans"
            )
        ]
    ])
    return keyboard
