from sqlalchemy.ext.asyncio import AsyncSession
from app.model.room import Room
from app.crud import crud_room
from app.schemas.room_schema import RoomCreate, RoomUpdate


async def list_all(db: AsyncSession) -> list[Room]:
    return await crud_room.get_all(db)


async def list_available(db: AsyncSession) -> list[Room]:
    return await crud_room.get_available(db)


async def list_booked(db: AsyncSession) -> list[Room]:
    return await crud_room.get_booked(db)


async def create_room(db: AsyncSession, data: RoomCreate) -> Room:
    existing = await crud_room.get_by_room_number(db, data.room_number)
    if existing:
        raise ValueError(f"房间号 {data.room_number} 已存在")
    room = Room(room_number=data.room_number, type=data.type, price=data.price, status=0)
    return await crud_room.create(db, room)


async def update_room(db: AsyncSession, room_id: int, data: RoomUpdate) -> Room:
    room = await crud_room.get_by_id(db, room_id)
    if not room:
        raise ValueError(f"房间 id={room_id} 不存在")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(room, field, value)

    await db.flush()
    await db.refresh(room)
    return room


async def delete_room(db: AsyncSession, room_id: int) -> None:
    ok = await crud_room.delete_by_id(db, room_id)
    if not ok:
        raise ValueError(f"房间 id={room_id} 不存在")


async def get_status_count(db: AsyncSession) -> dict:
    return await crud_room.get_status_count(db)


async def get_by_room_number(db: AsyncSession, room_number: int) -> Room | None:
    """按房间号查询"""
    return await crud_room.get_by_room_number(db, room_number)
