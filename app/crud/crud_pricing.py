from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.model.pricing import PriceHistory
from app.model.room import Room


async def get_all_rooms(db: AsyncSession) -> list[Room]:
    result = await db.execute(select(Room).order_by(Room.room_number))
    return list(result.scalars().all())


async def get_rooms_by_type(db: AsyncSession, room_type: str) -> list[Room]:
    result = await db.execute(
        select(Room).where(Room.type == room_type).order_by(Room.room_number)
    )
    return list(result.scalars().all())


async def update_room_price(db: AsyncSession, room_id: int, new_price: float) -> None:
    room = await db.get(Room, room_id)
    if room:
        room.price = new_price
        await db.flush()


async def add_price_history(db: AsyncSession, record: PriceHistory) -> PriceHistory:
    db.add(record)
    await db.flush()
    await db.refresh(record)
    return record


async def get_price_history(db: AsyncSession, limit: int = 50) -> list[PriceHistory]:
    result = await db.execute(
        select(PriceHistory).order_by(PriceHistory.id.desc()).limit(limit)
    )
    return list(result.scalars().all())
