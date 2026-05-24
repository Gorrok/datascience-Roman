from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base

class InviteStatus(enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"

class PlanType(enum.Enum):
    WISH = "wish"  # Хотелка
    PLAN = "plan"  # Конкретный план

class Plan(Base):
    __tablename__ = "plans"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000))
    plan_type = Column(Enum(PlanType), default=PlanType.WISH)
    
    # Кто создал
    created_by_id = Column(Integer, nullable=False)
    created_by_name = Column(String(100))
    
    # Дата планирования
    planned_date = Column(DateTime, nullable=True)
    
    # Статус
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    
    # Временные метки
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    invites = relationship("Invite", back_populates="plan", cascade="all, delete-orphan")

class Invite(Base):
    __tablename__ = "invites"
    
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)
    
    # Кто пригласил
    from_user_id = Column(Integer, nullable=False)
    from_user_name = Column(String(100))
    
    # Кого пригласили
    to_user_id = Column(Integer, nullable=False)
    to_user_name = Column(String(100))
    
    # Статус
    status = Column(Enum(InviteStatus), default=InviteStatus.PENDING)
    
    # Временные метки
    created_at = Column(DateTime, default=datetime.utcnow)
    responded_at = Column(DateTime, nullable=True)
    
    # Relationship
    plan = relationship("Plan", back_populates="invites")
