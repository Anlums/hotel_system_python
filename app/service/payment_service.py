from sqlalchemy.ext.asyncio import AsyncSession
from app.model.payment import Payment
from app.model.booking import Booking
from app.model.room import Room
from app.crud import crud_payment, crud_booking, crud_room
from decimal import Decimal
from datetime import datetime


async def collect_deposit(db: AsyncSession, booking_id: int, amount: Decimal,
                          method: str = "cash", remark: str = None, operator: str = "前台") -> Payment:
    """入住时收取押金"""
    booking = await crud_booking.get_by_id(db, booking_id)
    if not booking:
        raise ValueError(f"订单 id={booking_id} 不存在")
    if booking.status != 1:
        raise ValueError("只有已预约的订单才能收取押金")

    if amount <= 0:
        raise ValueError("押金金额必须大于 0")

    payment = Payment(
        booking_id=booking_id,
        type="deposit",
        amount=amount,
        method=method,
        status="completed",
        remark=remark or f"入住押金",
        operator=operator,
    )
    return await crud_payment.create(db, payment)


async def settle_bill(db: AsyncSession, booking_id: int,
                      method: str = "cash", remark: str = None, operator: str = "前台") -> list[Payment]:
    """退房结算：计算房费，扣除押金，生成最终支付/退款记录"""
    booking = await crud_booking.get_by_id(db, booking_id)
    if not booking:
        raise ValueError(f"订单 id={booking_id} 不存在")
    if booking.status != 2:
        raise ValueError("只有已入住的订单才能结算")

    # 获取房间单价
    room = await crud_room.get_by_room_number(db, booking.room_number)
    if not room:
        raise ValueError(f"房间号 {booking.room_number} 不存在")

    # 计算实际入住天数
    now = datetime.now()
    days = (now - booking.check_in_date).days
    if days <= 0:
        days = 1

    # 计算总房费
    total_amount = room.price * Decimal(str(days))

    # 获取已缴纳的押金总额
    deposit_total = await crud_payment.get_deposit_total(db, booking_id)
    deposit_decimal = Decimal(str(deposit_total))

    results = []

    if deposit_decimal >= total_amount:
        # 押金足够：押金扣房费，剩余退款
        refund_amount = deposit_decimal - total_amount
        if refund_amount > 0:
            refund = Payment(
                booking_id=booking_id,
                type="refund",
                amount=-refund_amount,
                method=method,
                status="completed",
                remark=remark or f"退房退款（押金{deposit_total} - 房费{total_amount}）",
                operator=operator,
            )
            results.append(await crud_payment.create(db, refund))
    else:
        # 押金不够：收房费 - 已交押金
        pay_amount = total_amount - deposit_decimal
        payment = Payment(
            booking_id=booking_id,
            type="payment",
            amount=pay_amount,
            method=method,
            status="completed",
            remark=remark or f"退房补交房费（总{total_amount} - 押金{deposit_total}）",
            operator=operator,
        )
        results.append(await crud_payment.create(db, payment))

    return results


async def list_payments(db: AsyncSession, booking_id: int = None) -> list[Payment]:
    return await crud_payment.get_all(db, booking_id)


async def get_stats(db: AsyncSession) -> dict:
    return await crud_payment.get_stats(db)
