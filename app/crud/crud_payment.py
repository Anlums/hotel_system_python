from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.model.payment import Payment


async def get_all(db: AsyncSession, booking_id: int = None) -> list[Payment]:
    query = select(Payment).order_by(Payment.id.desc())
    if booking_id is not None:
        query = query.where(Payment.booking_id == booking_id)
    result = await db.execute(query)
    return list(result.scalars().all())


async def create(db: AsyncSession, payment: Payment) -> Payment:
    db.add(payment)
    await db.flush()
    await db.refresh(payment)
    return payment


async def get_deposit_total(db: AsyncSession, booking_id: int) -> float:
    """获取某个订单的押金总额"""
    result = await db.execute(
        select(func.coalesce(func.sum(Payment.amount), 0))
        .where(Payment.booking_id == booking_id, Payment.type == "deposit", Payment.status == "completed")
    )
    return float(result.scalar() or 0)


async def get_stats(db: AsyncSession) -> dict:
    """获取支付统计"""
    # 总押金
    deposit = await db.execute(
        select(func.coalesce(func.sum(Payment.amount), 0))
        .where(Payment.type == "deposit", Payment.status == "completed")
    )
    # 总房费
    payment = await db.execute(
        select(func.coalesce(func.sum(Payment.amount), 0))
        .where(Payment.type == "payment", Payment.status == "completed")
    )
    # 总退款
    refund = await db.execute(
        select(func.coalesce(func.sum(Payment.amount), 0))
        .where(Payment.type == "refund", Payment.status == "completed")
    )
    total_deposit = float(deposit.scalar() or 0)
    total_payment = float(payment.scalar() or 0)
    total_refund = float(refund.scalar() or 0)
    return {
        "total_deposit": total_deposit,
        "total_payment": total_payment,
        "total_refund": abs(total_refund),
        "net_income": total_payment - abs(total_refund),
    }
