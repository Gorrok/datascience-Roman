from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from enum import Enum

class PlanType(str, Enum):
    WISH = "wish"
    PLAN = "plan"

class InviteStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"

# Plan schemas
class PlanBase(BaseModel):
    title: str
    description: Optional[str] = None
    plan_type: PlanType = PlanType.WISH
    planned_date: Optional[datetime] = None

class PlanCreate(PlanBase):
    created_by_id: int
    created_by_name: str

class PlanUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    planned_date: Optional[datetime] = None
    is_completed: Optional[bool] = None

class PlanResponse(PlanBase):
    id: int
    created_by_id: int
    created_by_name: str
    is_completed: bool
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Invite schemas
class InviteCreate(BaseModel):
    plan_id: int
    from_user_id: int
    from_user_name: str
    to_user_id: int
    to_user_name: str

class InviteResponse(BaseModel):
    id: int
    plan_id: int
    from_user_id: int
    from_user_name: str
    to_user_id: int
    to_user_name: str
    status: InviteStatus
    created_at: datetime
    responded_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
