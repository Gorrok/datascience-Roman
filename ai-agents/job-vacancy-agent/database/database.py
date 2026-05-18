"""
Database connection and session management
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from config import config
from database.models import Base
import logging

logger = logging.getLogger(__name__)

# Async engine
engine = create_async_engine(
    config.database_url,
    echo=False,  # Set to True for SQL query logging
    poolclass=NullPool,  # Для SQLite не нужен pool
)

# Session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db():
    """Создать все таблицы в БД"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✓ База данных инициализирована")


async def get_db() -> AsyncSession:
    """Dependency для получения сессии БД"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Ошибка при работе с БД: {e}")
            raise
        finally:
            await session.close()


async def close_db():
    """Закрыть соединение с БД"""
    await engine.dispose()
    logger.info("✓ Соединение с БД закрыто")
