"""
Сервис для работы с платежами через Stripe
"""
import stripe
from typing import Dict, Any, Optional
from loguru import logger
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.core.config import settings
from app.models.user import User
from app.models.subscription import Subscription

# Инициализация Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentService:
    """Сервис для работы с платежами"""
    
    # Цены тарифов (в центах)
    PRICING = {
        "trial": 0,
        "starter": 2900,  # $29.00
        "professional": 9900,  # $99.00
        "enterprise": 29900,  # $299.00
    }
    
    # Лимиты тарифов
    LIMITS = {
        "trial": {
            "max_bots": 1,
            "max_channels": 2,
            "has_api_access": False,
            "history_days": 30,
        },
        "starter": {
            "max_bots": 3,
            "max_channels": 10,
            "has_api_access": False,
            "history_days": 90,
        },
        "professional": {
            "max_bots": 10,
            "max_channels": 50,
            "has_api_access": True,
            "history_days": 365,
        },
        "enterprise": {
            "max_bots": 999,
            "max_channels": 999,
            "has_api_access": True,
            "history_days": 999999,
        },
    }
    
    @staticmethod
    def create_customer(user: User) -> str:
        """Создает customer в Stripe"""
        try:
            customer = stripe.Customer.create(
                email=user.email,
                name=user.full_name,
                metadata={
                    "user_id": user.id
                }
            )
            logger.info(f"✅ Создан Stripe customer {customer.id} для пользователя {user.id}")
            return customer.id
        except Exception as e:
            logger.error(f"❌ Ошибка создания Stripe customer: {e}")
            raise
    
    @staticmethod
    def create_checkout_session(
        user: User,
        plan_type: str,
        success_url: str,
        cancel_url: str,
        db: Session
    ) -> Dict[str, Any]:
        """Создает Checkout Session для подписки"""
        try:
            # Получаем или создаем Stripe customer
            subscription = db.query(Subscription).filter(
                Subscription.user_id == user.id
            ).first()
            
            if not subscription or not subscription.stripe_customer_id:
                customer_id = PaymentService.create_customer(user)
                
                if not subscription:
                    # Создаем подписку если её нет
                    subscription = Subscription(
                        user_id=user.id,
                        plan_type="trial",
                        stripe_customer_id=customer_id,
                        is_active=True,
                        **PaymentService.LIMITS["trial"]
                    )
                    db.add(subscription)
                else:
                    subscription.stripe_customer_id = customer_id
                
                db.commit()
            
            # Создаем Checkout Session
            session = stripe.checkout.Session.create(
                customer=subscription.stripe_customer_id,
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f'Telegram Analytics - {plan_type.title()}',
                        },
                        'unit_amount': PaymentService.PRICING[plan_type],
                        'recurring': {
                            'interval': 'month',
                        },
                    },
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={
                    'user_id': user.id,
                    'plan_type': plan_type,
                }
            )
            
            logger.info(f"✅ Создана Checkout Session {session.id} для пользователя {user.id}")
            
            return {
                "session_id": session.id,
                "url": session.url,
            }
        
        except Exception as e:
            logger.error(f"❌ Ошибка создания Checkout Session: {e}")
            raise
    
    @staticmethod
    def handle_checkout_completed(session: Dict[str, Any], db: Session):
        """Обрабатывает успешную оплату"""
        try:
            user_id = int(session['metadata']['user_id'])
            plan_type = session['metadata']['plan_type']
            stripe_subscription_id = session['subscription']
            
            # Обновляем подписку пользователя
            subscription = db.query(Subscription).filter(
                Subscription.user_id == user_id
            ).first()
            
            if subscription:
                subscription.plan_type = plan_type
                subscription.stripe_subscription_id = stripe_subscription_id
                subscription.is_active = True
                subscription.start_date = datetime.utcnow()
                subscription.end_date = None  # Подписка активна до отмены
                
                # Устанавливаем лимиты
                limits = PaymentService.LIMITS[plan_type]
                subscription.max_bots = limits["max_bots"]
                subscription.max_channels = limits["max_channels"]
                subscription.has_api_access = limits["has_api_access"]
                subscription.history_days = limits["history_days"]
                
                db.commit()
                
                logger.info(f"✅ Подписка пользователя {user_id} обновлена на {plan_type}")
        
        except Exception as e:
            logger.error(f"❌ Ошибка обработки checkout.session.completed: {e}")
            raise
    
    @staticmethod
    def handle_subscription_deleted(subscription_data: Dict[str, Any], db: Session):
        """Обрабатывает отмену подписки"""
        try:
            stripe_subscription_id = subscription_data['id']
            
            # Находим подписку
            subscription = db.query(Subscription).filter(
                Subscription.stripe_subscription_id == stripe_subscription_id
            ).first()
            
            if subscription:
                subscription.is_active = False
                subscription.end_date = datetime.utcnow()
                db.commit()
                
                logger.info(f"✅ Подписка {stripe_subscription_id} деактивирована")
        
        except Exception as e:
            logger.error(f"❌ Ошибка обработки customer.subscription.deleted: {e}")
            raise
    
    @staticmethod
    def cancel_subscription(user: User, db: Session) -> bool:
        """Отменяет подписку пользователя"""
        try:
            subscription = db.query(Subscription).filter(
                Subscription.user_id == user.id
            ).first()
            
            if not subscription or not subscription.stripe_subscription_id:
                return False
            
            # Отменяем подписку в Stripe
            stripe.Subscription.delete(subscription.stripe_subscription_id)
            
            # Обновляем в БД
            subscription.is_active = False
            subscription.end_date = datetime.utcnow()
            db.commit()
            
            logger.info(f"✅ Подписка пользователя {user.id} отменена")
            return True
        
        except Exception as e:
            logger.error(f"❌ Ошибка отмены подписки: {e}")
            return False
    
    @staticmethod
    def get_customer_portal_url(user: User, return_url: str, db: Session) -> Optional[str]:
        """Создает ссылку на Customer Portal для управления подпиской"""
        try:
            subscription = db.query(Subscription).filter(
                Subscription.user_id == user.id
            ).first()
            
            if not subscription or not subscription.stripe_customer_id:
                return None
            
            session = stripe.billing_portal.Session.create(
                customer=subscription.stripe_customer_id,
                return_url=return_url,
            )
            
            return session.url
        
        except Exception as e:
            logger.error(f"❌ Ошибка создания portal session: {e}")
            return None
