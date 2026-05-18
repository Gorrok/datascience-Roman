"""
SQLAlchemy модели для Job Vacancy Agent
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, ARRAY
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Channel(Base):
    """Telegram канал для мониторинга"""
    __tablename__ = "channels"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255))
    active = Column(Boolean, default=True)
    last_check = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    vacancies = relationship("Vacancy", back_populates="channel")
    
    def __repr__(self):
        return f"<Channel(username='{self.username}', active={self.active})>"


class Vacancy(Base):
    """Вакансия найденная в каналах"""
    __tablename__ = "vacancies"
    
    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, ForeignKey("channels.id"), nullable=False)
    
    # Извлеченные данные
    title = Column(Text)
    description = Column(Text)
    raw_text = Column(Text, nullable=False)  # Оригинальный текст сообщения
    requirements = Column(Text)  # JSON массив требований
    salary = Column(String(255))
    location = Column(String(255))
    company = Column(String(255))
    work_mode = Column(String(50))  # remote/office/hybrid
    
    # Анализ релевантности
    relevance_score = Column(Float, default=0.0)  # 0.0 - 1.0
    is_relevant = Column(Boolean, default=False)
    match_reason = Column(Text)  # Почему подходит/не подходит
    
    # Метаданные
    message_link = Column(String(500))  # Ссылка на сообщение в Telegram
    posted_at = Column(DateTime)  # Когда была опубликована
    found_at = Column(DateTime, default=datetime.utcnow)  # Когда нашли
    sent_to_user = Column(Boolean, default=False)  # Отправлена ли пользователю
    sent_at = Column(DateTime)  # Когда отправлена
    
    # Relationships
    channel = relationship("Channel", back_populates="vacancies")
    
    def __repr__(self):
        return f"<Vacancy(title='{self.title}', relevance={self.relevance_score:.2f})>"


class UserProfile(Base):
    """Профиль пользователя для фильтрации вакансий"""
    __tablename__ = "user_profile"
    
    id = Column(Integer, primary_key=True)
    
    # Навыки и опыт
    skills = Column(Text)  # JSON массив ["Python", "FastAPI"]
    experience_years = Column(Integer)
    
    # Предпочтения
    preferred_locations = Column(Text)  # JSON массив
    min_salary = Column(Integer)
    work_mode_preferences = Column(Text)  # JSON: ["remote", "hybrid"]
    
    # Фильтры
    keywords = Column(Text)  # JSON: Ключевые слова для поиска
    exclude_keywords = Column(Text)  # JSON: Исключающие слова
    
    # Метаданные
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<UserProfile(skills={self.skills}, experience={self.experience_years})>"


class ParseHistory(Base):
    """История парсинга каналов"""
    __tablename__ = "parse_history"
    
    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, ForeignKey("channels.id"))
    
    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime)
    
    messages_parsed = Column(Integer, default=0)
    vacancies_found = Column(Integer, default=0)
    relevant_vacancies = Column(Integer, default=0)
    
    status = Column(String(50))  # success/failed/partial
    error_message = Column(Text)
    
    def __repr__(self):
        return f"<ParseHistory(channel_id={self.channel_id}, status='{self.status}')>"
