from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_
from datetime import datetime
from typing import List

from app.core.database import get_db
from app.models.plan import Plan, Invite, InviteStatus as DBInviteStatus
from app.schemas.plan import (
    PlanCreate, PlanUpdate, PlanResponse,
    InviteCreate, InviteResponse, InviteStatus
)

router = APIRouter(prefix="/plans", tags=["plans"])

@router.post("/", response_model=PlanResponse)
async def create_plan(
    plan: PlanCreate,
    db: AsyncSession = Depends(get_db)
):
    """Создать новый план или хотелку"""
    db_plan = Plan(**plan.model_dump())
    db.add(db_plan)
    await db.commit()
    await db.refresh(db_plan)
    return db_plan

@router.get("/", response_model=List[PlanResponse])
async def get_plans(
    user_id: int,
    include_completed: bool = False,
    db: AsyncSession = Depends(get_db)
):
    """Получить все планы для пользователя"""
    query = select(Plan).where(
        or_(
            Plan.created_by_id == user_id,
            Plan.id.in_(
                select(Invite.plan_id).where(
                    and_(
                        Invite.to_user_id == user_id,
                        Invite.status == DBInviteStatus.ACCEPTED
                    )
                )
            )
        )
    )
    
    if not include_completed:
        query = query.where(Plan.is_completed == False)
    
    query = query.order_by(Plan.planned_date.asc().nulls_last())
    
    result = await db.execute(query)
    plans = result.scalars().all()
    return plans

@router.get("/{plan_id}", response_model=PlanResponse)
async def get_plan(
    plan_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Получить план по ID"""
    result = await db.execute(
        select(Plan).where(Plan.id == plan_id)
    )
    plan = result.scalar_one_or_none()
    
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    return plan

@router.patch("/{plan_id}", response_model=PlanResponse)
async def update_plan(
    plan_id: int,
    plan_update: PlanUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Обновить план"""
    result = await db.execute(
        select(Plan).where(Plan.id == plan_id)
    )
    plan = result.scalar_one_or_none()
    
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    update_data = plan_update.model_dump(exclude_unset=True)
    
    if "is_completed" in update_data and update_data["is_completed"]:
        update_data["completed_at"] = datetime.utcnow()
    
    for field, value in update_data.items():
        setattr(plan, field, value)
    
    await db.commit()
    await db.refresh(plan)
    return plan

@router.delete("/{plan_id}")
async def delete_plan(
    plan_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Удалить план"""
    result = await db.execute(
        select(Plan).where(Plan.id == plan_id)
    )
    plan = result.scalar_one_or_none()
    
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    await db.delete(plan)
    await db.commit()
    return {"message": "Plan deleted"}

# Invite endpoints
@router.post("/invites", response_model=InviteResponse)
async def create_invite(
    invite: InviteCreate,
    db: AsyncSession = Depends(get_db)
):
    """Отправить инвайт на план"""
    # Проверяем что план существует
    result = await db.execute(
        select(Plan).where(Plan.id == invite.plan_id)
    )
    plan = result.scalar_one_or_none()
    
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    # Создаем инвайт
    db_invite = Invite(**invite.model_dump())
    db.add(db_invite)
    await db.commit()
    await db.refresh(db_invite)
    return db_invite

@router.get("/invites/{user_id}", response_model=List[InviteResponse])
async def get_invites(
    user_id: int,
    status: InviteStatus = None,
    db: AsyncSession = Depends(get_db)
):
    """Получить инвайты для пользователя"""
    query = select(Invite).where(Invite.to_user_id == user_id)
    
    if status:
        db_status = DBInviteStatus[status.value.upper()]
        query = query.where(Invite.status == db_status)
    
    query = query.order_by(Invite.created_at.desc())
    
    result = await db.execute(query)
    invites = result.scalars().all()
    return invites

@router.patch("/invites/{invite_id}/respond")
async def respond_to_invite(
    invite_id: int,
    status: InviteStatus,
    db: AsyncSession = Depends(get_db)
):
    """Ответить на инвайт (принять/отклонить)"""
    result = await db.execute(
        select(Invite).where(Invite.id == invite_id)
    )
    invite = result.scalar_one_or_none()
    
    if not invite:
        raise HTTPException(status_code=404, detail="Invite not found")
    
    db_status = DBInviteStatus[status.value.upper()]
    invite.status = db_status
    invite.responded_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(invite)
    return {"message": f"Invite {status.value}"}
