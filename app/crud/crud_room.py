from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.model.room import Room

async def get_all(db: AsyncSession) -> list[Room]:
    result = await db.execute(select(Room).order_by(Room.room_number))
    return list(result.scalars().all())

async def get_available(db: AsyncSession) -> list[Room]:
    result = await db.execute(
        select(Room).where(Room.status == 0).order_by(Room.room_number)
    )
    return list(result.scalars().all())

async def get_booked(db: AsyncSession) -> list[Room]:
    result = await db.execute(
        select(Room).where(Room.status == 1).order_by(Room.room_number)
    )
    return list(result.scalars().all())

async def get_by_room_number(db: AsyncSession, room_number: int) -> Room | None:
    result = await db.execute(select(Room).where(Room.room_number == room_number))
    return result.scalar_one_or_none()

async def get_by_id(db: AsyncSession, room_id: int) -> Room | None:
    result = await db.execute(select(Room).where(Room.id == room_id))
    return result.scalar_one_or_none()

async def create(db: AsyncSession, room: Room) -> Room:
    """
    add - 标记对象待插入
    flush - 执行 INSERT 获取数据库生成的值
    refresh - 同步对象状态
    return - 返回完整对象
    :param db:
    :param room:
    :return:
    """

    db.add(room)
    await db.flush()       # 先 flush，保留事务控制权
    await db.refresh(room)
    return room
    # commit 由 FastAPI 依赖注入的 get_db() 在请求结束时自动处理

async def update_status(db: AsyncSession, room_number: int, status: int) -> None:
    await db.execute(
        update(Room).where(Room.room_number == room_number).values(status=status)
    )

async def delete_by_id(db: AsyncSession, room_id: int) -> bool:
    result = await db.execute(select(Room).where(Room.id == room_id))
    """
    scalar_one_or_none() - 期望返回 0 或 1 条记录
    找到 1 条 → 返回 Room 对象
    找到 0 条 → 返回 None
    找到多条 → 抛出异常（但 ID 是主键，不会出现）"""
    room = result.scalar_one_or_none()
    if not room:
        return False
    """
    不需要 await，因为这是同步操作（标记删除）
    真正的 DELETE 语句在 flush() 或 commit() 时执行
    由 FastAPI 的 get_db() 依赖在请求结束时自动 commit"""
    await db.delete(room)
    return True

async def get_status_count(db: AsyncSession) -> dict:
    """返回 {available, booked, occupied, cleaning}"""
    result = await db.execute(select(Room.status))
    rows = result.scalars().all()
    available = sum(1 for s in rows if s == 0)
    booked = sum(1 for s in rows if s == 1)
    occupied = sum(1 for s in rows if s == 2)
    cleaning = sum(1 for s in rows if s == 3)
    return {"available": available, "booked": booked, "occupied": occupied, "cleaning": cleaning}

