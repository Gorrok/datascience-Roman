"""
Celery конфигурация
"""
from celery import Celery
from app.core.config import settings

# Создаем экземпляр Celery
celery_app = Celery(
    "telegram_analytics",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

# Конфигурация
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 минут максимум на задачу
)

# Автоматически находим задачи
celery_app.autodiscover_tasks(["app.tasks"])
