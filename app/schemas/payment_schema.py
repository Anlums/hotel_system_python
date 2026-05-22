from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from typing import Optional


class DepositRequest(BaseModel):
    """收取押金请求"""
    booking_id: int
    amount: Decimal
    method: str = "cash"
    remark: Optional[str] = None
    operator: str = "前台"


class SettleRequest(BaseModel):
    """退房结算请求"""
    booking_id: int
    method: str = "cash"
    remark: Optional[str] = None
    operator: str = "前台"


class PaymentResponse(BaseModel):
    """支付记录"""
    id: int
    booking_id: int
    type: str
    amount: Decimal
    method: str
    status: str
    remark: Optional[str] = None
    operator: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class PaymentStatsResponse(BaseModel):
    """支付统计"""
    total_deposit: float = 0
    total_payment: float = 0
    total_refund: float = 0
    net_income: float = 0
