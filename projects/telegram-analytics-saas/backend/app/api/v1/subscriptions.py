"""
API endpoints для подписок и платежей
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
import stripe

from app.core.database import get_db, SessionLocal
from app.core.config import settings
from app.models.user import User
from app.api.v1.auth import get_current_user
from app.services.payment_service import PaymentService
from app.schemas.subscription import (
    SubscriptionResponse,
    CreateCheckoutSessionRequest,
    CreateCheckoutSessionResponse,
    CustomerPortalResponse
)

router = APIRouter()


@router.get("/me", response_model=SubscriptionResponse)
async def get_my_subscription(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Получить информацию о подписке текущего пользователя"""
    from app.models.subscription import Subscription
    
    result = await db.execute(
        select(Subscription).where(Subscription.user_id == current_user.id)
    )
    subscription = result.scalar_one_or_none()
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Подписка не найдена"
        )
    
    return subscription


@router.post("/checkout", response_model=CreateCheckoutSessionResponse)
async def create_checkout_session(
    request_data: CreateCheckoutSessionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Создать Stripe Checkout Session для оформления подписки"""
    
    # Валидируем план
    valid_plans = ["starter", "professional", "enterprise"]
    if request_data.plan_type not in valid_plans:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Недопустимый тип плана. Доступны: {', '.join(valid_plans)}"
        )
    
    try:
        # Используем sync session для Stripe
        sync_db = SessionLocal()
        
        result = PaymentService.create_checkout_session(
            user=current_user,
            plan_type=request_data.plan_type,
            success_url=request_data.success_url,
            cancel_url=request_data.cancel_url,
            db=sync_db
        )
        
        sync_db.close()
        
        return result
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка создания checkout session: {str(e)}"
        )


@router.post("/cancel")
async def cancel_subscription(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Отменить подписку"""
    
    try:
        sync_db = SessionLocal()
        success = PaymentService.cancel_subscription(current_user, sync_db)
        sync_db.close()
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Не удалось отменить подписку"
            )
        
        return {"message": "Подписка отменена"}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка отмены подписки: {str(e)}"
        )


@router.get("/portal", response_model=CustomerPortalResponse)
async def get_customer_portal(
    return_url: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Получить ссылку на Stripe Customer Portal"""
    
    try:
        sync_db = SessionLocal()
        url = PaymentService.get_customer_portal_url(current_user, return_url, sync_db)
        sync_db.close()
        
        if not url:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Не удалось создать ссылку на портал"
            )
        
        return {"url": url}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка создания portal session: {str(e)}"
        )


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    stripe_signature: Optional[str] = Header(None, alias="stripe-signature")
):
    """Webhook для обработки событий от Stripe"""
    
    if not stripe_signature:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Отсутствует stripe-signature"
        )
    
    payload = await request.body()
    
    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Невалидный payload"
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Невалидная подпись"
        )
    
    # Обрабатываем событие
    sync_db = SessionLocal()
    
    try:
        if event['type'] == 'checkout.session.completed':
            PaymentService.handle_checkout_completed(event['data']['object'], sync_db)
        
        elif event['type'] == 'customer.subscription.deleted':
            PaymentService.handle_subscription_deleted(event['data']['object'], sync_db)
        
        sync_db.close()
        
        return {"status": "success"}
    
    except Exception as e:
        sync_db.close()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка обработки webhook: {str(e)}"
        )
