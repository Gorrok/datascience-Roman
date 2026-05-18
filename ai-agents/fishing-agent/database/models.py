from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
import sys
import os

# Добавляем корневую директорию проекта в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import DATABASE_URL

Base = declarative_base()

class Lure(Base):
    """Модель для хранения инвентаря приманок."""
    __tablename__ = 'lures'
    id = Column(Integer, primary_key=True, index=True)
    lure_type = Column(String, index=True) # Тип: воблер, блесна, силикон
    brand = Column(String, index=True)
    model = Column(String, index=True)
    size = Column(String) # Размер (длина в см/мм)
    weight = Column(Float) # Вес в граммах
    color = Column(String)
    quantity = Column(Integer, default=1)
    condition = Column(String, default='новое') # Состояние: новое, б/у, требует замены
    
    catches = relationship("Catch", back_populates="lure")

class WaterBody(Base):
    """Модель для хранения информации о водоемах."""
    __tablename__ = 'water_bodies'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    type = Column(String) # Тип: река, озеро, водохранилище
    location = Column(String) # Регион или координаты
    
    sessions = relationship("FishingSession", back_populates="water_body")

class FishingSession(Base):
    """Модель для логирования рыболовных сессий."""
    __tablename__ = 'fishing_sessions'
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    water_body_id = Column(Integer, ForeignKey('water_bodies.id'))
    weather_conditions = Column(Text) # Давление, температура, ветер в JSON или текстом
    notes = Column(Text)

    water_body = relationship("WaterBody", back_populates="sessions")
    catches = relationship("Catch", back_populates="session")

class Catch(Base):
    """Модель для записи информации о каждой пойманной рыбе."""
    __tablename__ = 'catches'
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey('fishing_sessions.id'))
    fish_type = Column(String, index=True) # Вид рыбы
    lure_id = Column(Integer, ForeignKey('lures.id'))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    size_cm = Column(Float)
    weight_kg = Column(Float)

    session = relationship("FishingSession", back_populates="catches")
    lure = relationship("Lure", back_populates="catches")

class ScrapedData(Base):
    """Модель для хранения данных, собранных парсерами."""
    __tablename__ = 'scraped_data'
    id = Column(Integer, primary_key=True, index=True)
    source_type = Column(String, index=True) # Источник: forum, telegram, youtube
    source_url = Column(String, unique=True)
    content = Column(Text)
    extracted_info = Column(Text) # JSON с извлеченными данными
    processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class LureKnowledge(Base):
    """Модель для хранения энциклопедических знаний о приманках."""
    __tablename__ = 'lure_knowledge'
    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, index=True)
    model = Column(String, index=True)
    lure_type = Column(String, index=True)
    description = Column(Text)
    # Поля для хранения массивов данных в виде JSON или разделенных строк
    sizes = Column(String)
    weights = Column(String)
    target_fish = Column(String)
    source_url = Column(String, unique=True) # Ссылка на источник