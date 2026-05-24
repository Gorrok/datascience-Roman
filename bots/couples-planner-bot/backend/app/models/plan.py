from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base

class InviteStatus(enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"

class PlanType(enum.Enum):
    WISH = "wish"
    PLAN = "plan"

class Plan(Base):
    __tablename__ = "plans"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000))
    plan_type = Column(String(20), default="wish")
    
    created_by_id = Column(Integer, nullable=False)
    created_by_name = Column(String(100))
    
    planned_date = Column(DateTime, nullable=True)
    
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    invites = relationship("Invite", back_populates="plan", cascade="all, delete-orphan")

class Invite(Base):
    __tablename__ = "invites"
    
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)
    
    from_user_id = Column(Integer, nullable=False)
    from_user_name = Column(String(100))
    
    to_user_id = Column(Integer, nullable=False)
    to_user_name = Column(String(100))
    
    status = Column(String(20), default="pending")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    responded_at = Column(DateTime, nullable=True)
    
    plan = relationship("Plan", back_populates="invites")
