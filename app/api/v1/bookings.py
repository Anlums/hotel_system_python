from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.db.database import get_db
from app.service import booking_service
from app.schemas.booking_schema import BookingCreate, BookingUpdate, BookingResponse

router = APIRouter(prefix="/api/bookings", tags=["订单管理"])


@router.get("/list")
async def list_bookings(db: AsyncSession = Depends(get_db)):
    bookings = await booking_service.list_all(db)
    return {"code": 200, "data": [BookingResponse.model_validate(b) for b in bookings]}


@router.get("/search")
async def search_bookings(
    guest_name: Optional[str] = Query(None),
    room_number: Optional[int] = Query(None),
    status: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    bookings = await booking_service.search_bookings(db, guest_name, room_number, status)
    return {"code": 200, "data": [BookingResponse.model_validate(b) for b in bookings]}


@router.get("/findByName")
async def find_by_name(name: str, db: AsyncSession = Depends(get_db)):
    bookings = await booking_service.search_bookings(db, guest_name=name)
    return {"code": 200, "data": [BookingResponse.model_validate(b) for b in bookings]}


@router.post("/save")
async def save_booking(data: BookingCreate, db: AsyncSession = Depends(get_db)):
    try:
        bk = await booking_service.place_order(
            db, data.room_number, data.guest_name, data.phone,
            data.check_in_date, data.check_out_date
        )
        await db.commit()
        return {"code": 200, "data": BookingResponse.model_validate(bk)}
    except ValueError as e:
        return {"code": 500, "msg": str(e)}


@router.post("/placeOrder")
async def place_order(data: BookingCreate, db: AsyncSession = Depends(get_db)):
    try:
        bk = await booking_service.place_order(
            db, data.room_number, data.guest_name, data.phone,
            data.check_in_date, data.check_out_date
        )
        await db.commit()
        return {"code": 200, "data": BookingResponse.model_validate(bk)}
    except ValueError as e:
        return {"code": 500, "msg": str(e)}


@router.post("/add")
async def add_booking(data: BookingCreate, db: AsyncSession = Depends(get_db)):
    try:
        bk = await booking_service.place_order(
            db, data.room_number, data.guest_name, data.phone,
            data.check_in_date, data.check_out_date
        )
        await db.commit()
        return {"code": 200, "data": BookingResponse.model_validate(bk)}
    except ValueError as e:
        return {"code": 500, "msg": str(e)}


@router.put("/checkIn")
async def check_in(id: int, db: AsyncSession = Depends(get_db)):
    try:
        await booking_service.check_in(db, id)
        await db.commit()
        return {"code": 200, "msg": "办理入住成功"}
    except ValueError as e:
        return {"code": 500, "msg": str(e)}


@router.put("/checkOut")
async def check_out(id: int, db: AsyncSession = Depends(get_db)):
    try:
        await booking_service.check_out(db, id)
        await db.commit()
        return {"code": 200, "msg": f"id为{id}的订单已退房"}
    except ValueError as e:
        return {"code": 500, "msg": str(e)}


@router.put("/cancel")
async def cancel(id: int, db: AsyncSession = Depends(get_db)):
    try:
        await booking_service.cancel_booking(db, id)
        await db.commit()
        return {"code": 200, "msg": "订单已取消"}
    except ValueError as e:
        return {"code": 500, "msg": str(e)}


@router.put("/update")
async def update(id: int, data: BookingUpdate, db: AsyncSession = Depends(get_db)):
    try:
        bk = await booking_service.update_booking(db, id, data.model_dump(exclude_unset=True))
        await db.commit()
        return {"code": 200, "data": BookingResponse.model_validate(bk)}
    except ValueError as e:
        return {"code": 500, "msg": str(e)}


@router.delete("/delete")
async def delete(id: int, db: AsyncSession = Depends(get_db)):
    try:
        await booking_service.delete_booking(db, id)
        await db.commit()
        return {"code": 200, "msg": f"删除id为{id}的订单成功"}
    except ValueError as e:
        return {"code": 500, "msg": str(e)}


@router.get("/revenue")
async def revenue(days: int = Query(default=7), db: AsyncSession = Depends(get_db)):
    data = await booking_service.get_daily_revenue(db, days)
    return {"code": 200, "data": data}
