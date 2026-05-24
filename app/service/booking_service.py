from sqlalchemy.ext.asyncio import AsyncSession
from app.model.booking import Booking
from app.model.room import Room
from app.model.cleaning_task import CleaningTask
from app.crud import crud_booking, crud_room
from datetime import datetime, date, timedelta
from decimal import Decimal


def parse_dt(s: str) -> datetime:
    """解析日期时间字符串，兼容多种格式"""
    if not s or not s.strip():
        raise ValueError("日期时间不能为空")
    s = s.strip().replace('T', ' ')
    for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"]:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    raise ValueError(f"无法解析日期时间: {s}")


async def list_all(db: AsyncSession) -> list[Booking]:
    return await crud_booking.get_all(db)


async def search_bookings(db: AsyncSession, guest_name: str = None,
                          room_number: int = None, status: int = None) -> list[Booking]:
    return await crud_booking.search(db, guest_name, room_number, status)


async def place_order(db: AsyncSession, room_number: int, guest_name: str,
                      phone: str, check_in: str, check_out: str = None) -> Booking:
    """下单预订"""
    room = await crud_room.get_by_room_number(db,  room_number)
    if not room:
        raise ValueError(f"房间号 {room_number} 不存在")
    if room.status == 1:
        raise ValueError(f"房间号 {room_number} 已被占用")

    check_in_dt = parse_dt(check_in)
    # 退房日期为空则默认+1天
    if not check_out:
        check_out_dt = check_in_dt.replace(hour=12, minute=0, second=0) + timedelta(days=1)
    else:
        check_out_dt = parse_dt(check_out)

    booking = Booking(
        room_number=room_number,
        guest_name=guest_name,
        phone=phone,
        check_in_date=check_in_dt,
        check_out_date=check_out_dt,
        total_amount=Decimal("0"),
        status=1,
    )
    new_booking = await crud_booking.create(db, booking)
    await crud_room.update_status(db, room_number, 1)
    return new_booking


async def check_in(db: AsyncSession, booking_id: int) -> None:
    """办理入住: 订单状态 1→2, 房间状态 1→2"""
    booking = await crud_booking.get_by_id(db, booking_id)
    if not booking:
        raise ValueError(f"订单 id={booking_id} 不存在")
    if booking.status != 1:
        raise ValueError("只有已预约的订单才能办理入住")
    booking.status = 2
    # 房间状态改为 2-已入住
    await crud_room.update_status(db, booking.room_number, 2)


async def check_out(db: AsyncSession, booking_id: int) -> None:
    """退房结算: 计算天数*房费, 状态设为3, 释放房间"""
    booking = await crud_booking.get_by_id(db, booking_id)
    if not booking:
        raise ValueError(f"订单 id={booking_id} 不存在")
    if booking.status == 4:
        raise ValueError("该订单已取消，无法退房")

    room = await crud_room.get_by_room_number(db, booking.room_number)
    if not room:
        raise ValueError(f"房间号 {booking.room_number} 不存在")

    now = datetime.now()
    days = (now - booking.check_in_date).days
    if days <= 0:
        days = 1

    booking.total_amount = room.price * Decimal(str(days))
    booking.status = 3
    booking.check_out_date = now
    # 房间状态改为 3-清洁中，并创建保洁工单
    await crud_room.update_status(db, booking.room_number, 3)
    cleaning_task = CleaningTask(room_number=booking.room_number, booking_id=booking.id, status=0)
    db.add(cleaning_task)


async def cancel_booking(db: AsyncSession, booking_id: int) -> None:
    """取消订单: 状态设为4, 释放房间"""
    booking = await crud_booking.get_by_id(db, booking_id)
    if not booking:
        raise ValueError(f"订单 id={booking_id} 不存在")
    booking.status = 4
    await crud_room.update_status(db, booking.room_number, 0)


async def update_booking(db: AsyncSession, booking_id: int, data: dict) -> Booking:
    """修改订单（支持换房）"""
    booking = await crud_booking.get_by_id(db, booking_id)
    if not booking:
        raise ValueError(f"订单 id={booking_id} 不存在")

    new_room_number = data.get("room_number")
    if new_room_number and new_room_number != booking.room_number:
        new_room = await crud_room.get_by_room_number(db, new_room_number)
        if not new_room:
            raise ValueError(f"新房间号 {new_room_number} 不存在")
        if new_room.status == 1:
            raise ValueError(f"新房间 {new_room_number} 已被占用")
        await crud_room.update_status(db, booking.room_number, 0)
        await crud_room.update_status(db, new_room_number, 1)

    for field, value in data.items():
        if hasattr(booking, field) and value is not None:
            # 日期字段：空字符串跳过，非空字符串转 datetime
            if field in ("check_in_date", "check_out_date"):
                if isinstance(value, str) and value.strip():
                    value = parse_dt(value)
                else:
                    continue  # 跳过空日期
            setattr(booking, field, value)

    await db.flush()
    await db.refresh(booking)
    return booking


async def delete_booking(db: AsyncSession, booking_id: int) -> None:
    """删除订单并释放房间"""
    booking = await crud_booking.get_by_id(db, booking_id)
    if not booking:
        raise ValueError(f"订单 id={booking_id} 不存在")
    await crud_room.update_status(db, booking.room_number, 0)
    await crud_booking.delete(db, booking_id)


async def get_daily_revenue(db: AsyncSession, days: int = 7) -> list[dict]:
    return await crud_booking.get_daily_revenue(db, days)
