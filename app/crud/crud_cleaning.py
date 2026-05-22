from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.model.cleaning_task import CleaningTask
from datetime import datetime


async def get_all(db: AsyncSession) -> list[CleaningTask]:
    result = await db.execute(select(CleaningTask).order_by(CleaningTask.id.desc()))
    return list(result.scalars().all())


async def get_pending(db: AsyncSession) -> list[CleaningTask]:
    """获取待清洁和清洁中的工单"""
    result = await db.execute(
        select(CleaningTask)
        .where(CleaningTask.status.in_([0, 1]))
        .order_by(CleaningTask.created_at.desc())
    )
    return list(result.scalars().all())


async def get_by_id(db: AsyncSession, task_id: int) -> CleaningTask | None:
    result = await db.execute(select(CleaningTask).where(CleaningTask.id == task_id))
    return result.scalar_one_or_none()


async def create(db: AsyncSession, task: CleaningTask) -> CleaningTask:
    db.add(task)
    await db.flush()
    await db.refresh(task)
    return task


async def assign(db: AsyncSession, task_id: int, assignee: str) -> CleaningTask | None:
    task = await get_by_id(db, task_id)
    if not task or task.status != 0:
        return None
    task.status = 1  # 清洁中
    task.assignee = assignee
    await db.flush()
    await db.refresh(task)
    return task


async def complete(db: AsyncSession, task_id: int) -> CleaningTask | None:
    task = await get_by_id(db, task_id)
    if not task:
        return None
    task.status = 2  # 已完成
    task.completed_at = datetime.now()
    await db.flush()
    await db.refresh(task)
    return task
