from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

# Добавляем корневую директорию проекта в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from .models import Base
from config import DATABASE_URL


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Инициализирует базу данных, создавая все необходимые таблицы.
    """
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")

def get_db():
    """
    Создает и возвращает сессию базы данных.
    Гарантирует закрытие сессии после использования.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    init_db()