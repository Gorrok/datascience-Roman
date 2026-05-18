"""
Главный файл FastAPI приложения
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.core.config import settings

# Создаем приложение
app = FastAPI(
    title=settings.APP_NAME,
    description="API для платформы аналитики Telegram каналов",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """События при старте приложения"""
    logger.info(f"🚀 {settings.APP_NAME} запущен")
    logger.info(f"📝 Документация доступна: /docs")
    logger.info(f"🌍 Окружение: {settings.ENVIRONMENT}")


@app.on_event("shutdown")
async def shutdown_event():
    """События при остановке приложения"""
    logger.info(f"👋 {settings.APP_NAME} остановлен")


@app.get("/")
async def root():
    """Корневой endpoint"""
    return {
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Импортируем роутеры
from app.api.v1 import auth, bots, channels, analytics, google_sheets, subscriptions

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(bots.router, prefix="/api/v1/bots", tags=["bots"])
app.include_router(channels.router, prefix="/api/v1/channels", tags=["channels"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])
app.include_router(google_sheets.router, prefix="/api/v1/google-sheets", tags=["google-sheets"])
app.include_router(subscriptions.router, prefix="/api/v1/subscriptions", tags=["subscriptions"])
