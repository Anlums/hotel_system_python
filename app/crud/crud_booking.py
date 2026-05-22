from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text, case
from app.model.booking import Booking
from datetime import datetime, date
from decimal import Decimal


async def get_all(db: AsyncSession) -> list[Booking]:
    status_order = case(
        (Booking.status == 1, 0),
        (Booking.status == 2, 1),
        (Booking.status == 3, 2),
        (Booking.status == 4, 3),
        else_=4
    )
    result = await db.execute(select(Booking).order_by(status_order, Booking.id.desc()))
    return list(result.scalars().all())


async def get_by_id(db: AsyncSession, booking_id: int) -> Booking | None:
    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    return result.scalar_one_or_none()


async def create(db: AsyncSession, booking: Booking) -> Booking:
    db.add(booking)
    await db.flush()
    await db.refresh(booking)
    return booking


async def delete(db: AsyncSession, booking_id: int) -> bool:
    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    booking = result.scalar_one_or_none()
    if not booking:
        return False
    await db.delete(booking)
    return True


async def search(db: AsyncSession, guest_name: str = None, room_number: int = None,
                 status: int = None) -> list[Booking]:
    query = select(Booking)
    if guest_name:
        query = query.where(Booking.guest_name.like(f"%{guest_name}%"))
    if room_number is not None:
        query = query.where(Booking.room_number == room_number)
    if status is not None:
        query = query.where(Booking.status == status)
    status_order = case(
        (Booking.status == 1, 0),
        (Booking.status == 2, 1),
        (Booking.status == 3, 2),
        (Booking.status == 4, 3),
        else_=4
    )
    query = query.order_by(status_order, Booking.id.desc())
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_daily_revenue(db: AsyncSession, days: int = 7) -> list[dict]:
    """返回近 N 天每日营收"""
    stmt = text("""
        SELECT DATE(check_out_date) as date, SUM(total_amount) as revenue
        FROM bookings
        WHERE status = 3 AND check_out_date >= DATE_SUB(CURDATE(), INTERVAL :days DAY)
        GROUP BY DATE(check_out_date)
        ORDER BY date
    """)
    result = await db.execute(stmt, {"days": days})
    rows = result.fetchall()
    return [{"date": str(row[0]), "revenue": float(row[1])} for row in rows]


async def get_conflicts(db: AsyncSession, room_number: int, check_in: str, check_out: str) -> list[Booking]:
    """检查某个房间在日期范围内是否有冲突订单（未退房/未取消）"""
    stmt = select(Booking).where(
        Booking.room_number == room_number,
        Booking.status.in_([1, 2]),  # 已预约或已入住
        Booking.check_in_date < check_out,
        Booking.check_out_date > check_in,
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())
