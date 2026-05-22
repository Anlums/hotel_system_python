from sqlalchemy.ext.asyncio import AsyncSession
from app.model.cleaning_task import CleaningTask
from app.crud import crud_cleaning, crud_room
from app.schemas.cleaning_schema import CleaningTaskResponse


async def list_all(db: AsyncSession) -> list[CleaningTask]:
    return await crud_cleaning.get_all(db)


async def list_pending(db: AsyncSession) -> list[CleaningTask]:
    return await crud_cleaning.get_pending(db)


async def create_task(db: AsyncSession, room_number: int, booking_id: int = None) -> CleaningTask:
    """退房时自动创建保洁工单，房间状态改为 3-清洁中"""
    task = CleaningTask(room_number=room_number, booking_id=booking_id, status=0)
    new_task = await crud_cleaning.create(db, task)
    await crud_room.update_status(db, room_number, 3)  # 清洁中
    return new_task


async def assign_task(db: AsyncSession, task_id: int, assignee: str) -> CleaningTask:
    task = await crud_cleaning.assign(db, task_id, assignee)
    if not task:
        raise ValueError("工单不存在或已被领取")
    return task


async def complete_task(db: AsyncSession, task_id: int) -> CleaningTask:
    """保洁完成 → 房间状态恢复为 0-空闲"""
    task = await crud_cleaning.get_by_id(db, task_id)
    if not task:
        raise ValueError("工单不存在")

    task = await crud_cleaning.complete(db, task_id)
    if not task:
        raise ValueError("工单不存在")

    # 房间恢复空闲
    await crud_room.update_status(db, task.room_number, 0)
    return task
