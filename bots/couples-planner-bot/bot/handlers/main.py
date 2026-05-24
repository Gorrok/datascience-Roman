from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from datetime import datetime
from loguru import logger

from keyboards.inline import get_main_menu, get_invite_keyboard, get_plan_keyboard
from utils.api_client import APIClient

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, api_client: APIClient, mini_app_url: str):
    """Обработчик команды /start"""
    await message.answer(
        f"Привет, {message.from_user.first_name}\n\n"
        f"Ваш личный планировщик для пары\n\n"
        f"Возможности:\n"
        f"• Записывать планы и хотелки\n"
        f"• Назначать их на даты\n"
        f"• Приглашать друг друга на планы\n"
        f"• Отмечать выполненное\n\n"
        f"Откройте приложение через кнопку ниже:",
        reply_markup=get_main_menu(mini_app_url)
    )

@router.callback_query(F.data == "my_plans")
async def show_my_plans(callback: CallbackQuery, api_client: APIClient):
    """Показать планы пользователя"""
    await callback.answer()
    
    plans = await api_client.get_plans(callback.from_user.id)
    
    if not plans:
        await callback.message.edit_text(
            "У вас пока нет планов.\n"
            "Откройте приложение чтобы добавить первый план! 🎯"
        )
        return
    
    text = "📋 Ваши планы:\n\n"
    
    for plan in plans[:10]:  # Показываем только первые 10
        planned_date = plan.get("planned_date")
        date_str = ""
        if planned_date:
            date = datetime.fromisoformat(planned_date.replace("Z", "+00:00"))
            date_str = f" 📅 {date.strftime('%d.%m.%Y')}"
        
        text += f"• {plan['title']}{date_str}\n"
    
    if len(plans) > 10:
        text += f"\n... и еще {len(plans) - 10} планов"
    
    await callback.message.edit_text(text)

@router.callback_query(F.data == "my_invites")
async def show_my_invites(callback: CallbackQuery, api_client: APIClient):
    """Показать инвайты пользователя"""
    await callback.answer()
    
    invites = await api_client.get_invites(callback.from_user.id, status="pending")
    
    if not invites:
        await callback.message.edit_text(
            "У вас нет новых приглашений 📭"
        )
        return
    
    invite = invites[0]  # Показываем первое приглашение
    
    text = (
        f"💌 Приглашение от {invite['from_user_name']}!\n\n"
        f"📝 {invite['plan']['title']}\n"
    )
    
    if invite['plan'].get('description'):
        text += f"\n{invite['plan']['description']}\n"
    
    if invite['plan'].get('planned_date'):
        date = datetime.fromisoformat(invite['plan']['planned_date'].replace("Z", "+00:00"))
        text += f"\n📅 {date.strftime('%d.%m.%Y в %H:%M')}\n"
    
    await callback.message.edit_text(
        text,
        reply_markup=get_invite_keyboard(invite['id'])
    )

@router.callback_query(F.data.startswith("invite_accept_"))
async def accept_invite(callback: CallbackQuery, api_client: APIClient):
    """Принять приглашение"""
    invite_id = int(callback.data.split("_")[2])
    
    success = await api_client.respond_to_invite(invite_id, "accepted")
    
    if success:
        await callback.answer("✅ Приглашение принято!")
        await callback.message.edit_text(
            "✅ Приглашение принято!\n"
            "План добавлен в ваш список."
        )
    else:
        await callback.answer("❌ Ошибка при принятии приглашения", show_alert=True)

@router.callback_query(F.data.startswith("invite_decline_"))
async def decline_invite(callback: CallbackQuery, api_client: APIClient):
    """Отклонить приглашение"""
    invite_id = int(callback.data.split("_")[2])
    
    success = await api_client.respond_to_invite(invite_id, "declined")
    
    if success:
        await callback.answer("❌ Приглашение отклонено")
        await callback.message.edit_text("❌ Приглашение отклонено")
    else:
        await callback.answer("❌ Ошибка при отклонении приглашения", show_alert=True)

@router.callback_query(F.data.startswith("plan_complete_"))
async def complete_plan(callback: CallbackQuery, api_client: APIClient):
    """Отметить план как выполненный"""
    plan_id = int(callback.data.split("_")[2])
    
    success = await api_client.complete_plan(plan_id)
    
    if success:
        await callback.answer("✅ План выполнен!")
        await callback.message.edit_text(
            "✅ Отлично! План отмечен как выполненный 🎉"
        )
    else:
        await callback.answer("❌ Ошибка при обновлении плана", show_alert=True)
