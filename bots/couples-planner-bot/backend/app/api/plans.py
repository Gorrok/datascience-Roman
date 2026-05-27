from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_
from sqlalchemy.orm import selectinload
from datetime import datetime
from typing import List

from app.core.config import settings
from app.core.database import get_db
from app.models.plan import Plan, Invite
from app.schemas.plan import (
    PlanCreate, PlanUpdate, PlanResponse,
    InviteCreate, InviteResponse, InviteStatus
)
from app.services.notifier import (
    notify_invite,
    notify_invite_response,
    notify_partner_about_plan,
)

router = APIRouter(prefix="/plans", tags=["plans"])


def _partner_id(user_id: int) -> int | None:
    if settings.USER_1_ID and settings.USER_2_ID:
        if user_id == settings.USER_1_ID:
            return settings.USER_2_ID
        if user_id == settings.USER_2_ID:
            return settings.USER_1_ID
    return None


@router.post("/", response_model=PlanResponse)
async def create_plan(
    plan: PlanCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """Создать новый план или хотелку"""
    db_plan = Plan(**plan.model_dump())
    db.add(db_plan)
    await db.commit()
    await db.refresh(db_plan)

    partner_id = _partner_id(db_plan.created_by_id)
    if partner_id:
        background_tasks.add_task(
            notify_partner_about_plan,
            partner_id,
            db_plan.created_by_name,
            db_plan.title,
            db_plan.plan_type,
        )

    return db_plan

@router.get("/", response_model=List[PlanResponse])
async def get_plans(
    user_id: int,
    include_completed: bool = False,
    only_completed: bool = False,
    db: AsyncSession = Depends(get_db)
):
    """Получить все планы для пользователя.

    - `include_completed`: вернуть и активные, и выполненные
    - `only_completed`: вернуть только выполненные (история)
    """
    query = select(Plan).where(
        or_(
            Plan.created_by_id == user_id,
            Plan.id.in_(
                select(Invite.plan_id).where(
                    and_(
                        Invite.to_user_id == user_id,
                        Invite.status == "accepted"
                    )
                )
            )
        )
    )

    if only_completed:
        query = query.where(Plan.is_completed == True)
        query = query.order_by(Plan.completed_at.desc().nulls_last())
    elif not include_completed:
        query = query.where(Plan.is_completed == False)
        query = query.order_by(Plan.planned_date.asc().nulls_last())
    else:
        query = query.order_by(Plan.is_completed.asc(), Plan.planned_date.asc().nulls_last())

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/stats/{user_id}")
async def get_stats(user_id: int, db: AsyncSession = Depends(get_db)):
    """Собрать сводную статистику для пары."""
    base = select(Plan).where(
        or_(
            Plan.created_by_id == user_id,
            Plan.id.in_(
                select(Invite.plan_id).where(
                    and_(
                        Invite.to_user_id == user_id,
                        Invite.status == "accepted"
                    )
                )
            )
        )
    )
    result = await db.execute(base)
    plans = result.scalars().all()

    total = len(plans)
    completed = sum(1 for p in plans if p.is_completed)
    active = total - completed
    plans_count = sum(1 for p in plans if p.plan_type == "plan" and not p.is_completed)
    wishes_count = sum(1 for p in plans if p.plan_type == "wish" and not p.is_completed)

    pending_invites_q = select(Invite).where(
        and_(Invite.to_user_id == user_id, Invite.status == "pending")
    )
    pending_invites = (await db.execute(pending_invites_q)).scalars().all()

    return {
        "total": total,
        "completed": completed,
        "active": active,
        "plans": plans_count,
        "wishes": wishes_count,
        "pending_invites": len(pending_invites),
    }

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

    if "is_completed" in update_data:
        if update_data["is_completed"]:
            update_data["completed_at"] = datetime.utcnow()
        else:
            update_data["completed_at"] = None

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
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """Отправить инвайт на план"""
    result = await db.execute(
        select(Plan).where(Plan.id == invite.plan_id)
    )
    plan = result.scalar_one_or_none()

    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    db_invite = Invite(**invite.model_dump())
    db.add(db_invite)
    await db.commit()
    await db.refresh(db_invite)

    background_tasks.add_task(
        notify_invite,
        db_invite.to_user_id,
        db_invite.from_user_name,
        plan.title,
        db_invite.id,
    )

    return db_invite

@router.get("/invites/{user_id}", response_model=List[InviteResponse])
async def get_invites(
    user_id: int,
    status: InviteStatus = None,
    db: AsyncSession = Depends(get_db)
):
    """Получить инвайты для пользователя"""
    query = (
        select(Invite)
        .where(Invite.to_user_id == user_id)
        .options(selectinload(Invite.plan))
    )

    if status:
        query = query.where(Invite.status == status.value)

    query = query.order_by(Invite.created_at.desc())

    result = await db.execute(query)
    return result.scalars().all()

@router.patch("/invites/{invite_id}/respond")
async def respond_to_invite(
    invite_id: int,
    status: InviteStatus,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """Ответить на инвайт (принять/отклонить)"""
    result = await db.execute(
        select(Invite).where(Invite.id == invite_id)
    )
    invite = result.scalar_one_or_none()

    if not invite:
        raise HTTPException(status_code=404, detail="Invite not found")

    invite.status = status.value
    invite.responded_at = datetime.utcnow()

    await db.commit()
    await db.refresh(invite)

    plan_q = await db.execute(select(Plan).where(Plan.id == invite.plan_id))
    plan = plan_q.scalar_one_or_none()
    if plan:
        background_tasks.add_task(
            notify_invite_response,
            invite.from_user_id,
            invite.to_user_name,
            plan.title,
            status.value == "accepted",
        )

    return {"message": f"Invite {status.value}"}
