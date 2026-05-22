from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.service import room_service
from app.schemas.room_schema import RoomCreate, RoomUpdate, RoomResponse

router = APIRouter(prefix="/api/rooms", tags=["房间管理"])


@router.get("/allRoom", response_model=list[RoomResponse])
async def list_rooms(db: AsyncSession = Depends(get_db)):
    return await room_service.list_all(db)


@router.get("/availableRooms", response_model=list[RoomResponse])
async def available_rooms(db: AsyncSession = Depends(get_db)):
    return await room_service.list_available(db)


@router.get("/bookedRooms", response_model=list[RoomResponse])
async def booked_rooms(db: AsyncSession = Depends(get_db)):
    return await room_service.list_booked(db)


@router.get("/statusCount")
async def status_count(db: AsyncSession = Depends(get_db)):
    data = await room_service.get_status_count(db)
    return {"code": 200, "data": data}


@router.get("/get")
async def get_room(room_number: int, db: AsyncSession = Depends(get_db)):
    room = await room_service.get_by_room_number(db, room_number)
    if not room:
        return {"code": 404, "msg": "房间不存在"}
    return {"code": 200, "data": RoomResponse.model_validate(room)}


@router.post("/insertRoom")
async def insert_room(data: RoomCreate, db: AsyncSession = Depends(get_db)):
    try:
        room = await room_service.create_room(db, data)
        await db.commit()
        return {"code": 200, "msg": "新增成功", "data": RoomResponse.model_validate(room)}
    except ValueError as e:
        return {"code": 500, "msg": str(e)}


@router.put("/update")
async def update_room(room_id: int, data: RoomUpdate, db: AsyncSession = Depends(get_db)):
    try:
        room = await room_service.update_room(db, room_id, data)
        await db.commit()
        return {"code": 200, "data": RoomResponse.model_validate(room)}
    except ValueError as e:
        return {"code": 500, "msg": str(e)}


@router.delete("/delete")
async def delete_room(id: int, db: AsyncSession = Depends(get_db)):
    try:
        await room_service.delete_room(db, id)
        await db.commit()
        return {"code": 200, "msg": "房间删除成功"}
    except ValueError as e:
        return {"code": 500, "msg": str(e)}
