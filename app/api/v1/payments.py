from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.db.database import get_db
from app.service import payment_service
from app.schemas.payment_schema import DepositRequest, SettleRequest, PaymentResponse, PaymentStatsResponse

router = APIRouter(prefix="/api/payments", tags=["支付结算"])


@router.get("/list")
async def list_payments(booking_id: Optional[int] = Query(None), db: AsyncSession = Depends(get_db)):
    payments = await payment_service.list_payments(db, booking_id)
    return {"code": 200, "data": [PaymentResponse.model_validate(p) for p in payments]}


@router.get("/stats")
async def payment_stats(db: AsyncSession = Depends(get_db)):
    stats = await payment_service.get_stats(db)
    return {"code": 200, "data": stats}


@router.post("/deposit")
async def collect_deposit(data: DepositRequest, db: AsyncSession = Depends(get_db)):
    try:
        payment = await payment_service.collect_deposit(
            db, data.booking_id, data.amount, data.method, data.remark, data.operator
        )
        await db.commit()
        return {"code": 200, "msg": f"押金 ¥{data.amount} 已收取", "data": PaymentResponse.model_validate(payment)}
    except ValueError as e:
        return {"code": 500, "msg": str(e)}


@router.post("/settle")
async def settle_bill(data: SettleRequest, db: AsyncSession = Depends(get_db)):
    try:
        payments = await payment_service.settle_bill(
            db, data.booking_id, data.method, data.remark, data.operator
        )
        await db.commit()
        return {
            "code": 200,
            "msg": "结算完成",
            "data": [PaymentResponse.model_validate(p) for p in payments],
        }
    except ValueError as e:
        return {"code": 500, "msg": str(e)}
