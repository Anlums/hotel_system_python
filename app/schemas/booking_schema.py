from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from typing import Optional


class BookingCreate(BaseModel):
    """创建订单"""
    room_number: int
    guest_name: str
    phone: str
    check_in_date: str
    check_out_date: Optional[str] = None
    total_amount: Optional[Decimal] = None


class BookingUpdate(BaseModel):
    """修改订单"""
    room_number: Optional[int] = None
    guest_name: Optional[str] = None
    phone: Optional[str] = None
    check_in_date: Optional[str] = None
    check_out_date: Optional[str] = None


class BookingResponse(BaseModel):
    """返回给前端的订单信息"""
    id: int
    room_number: int
    guest_name: str
    phone: str
    check_in_date: datetime
    check_out_date: Optional[datetime] = None
    total_amount: Decimal
    status: int
    create_time: Optional[datetime] = None

    model_config = {"from_attributes": True}


class DailyRevenueResponse(BaseModel):
    """每日营收"""
    date: str
    revenue: Decimal


class RoomStatusCountResponse(BaseModel):
    """房间状态统计"""
    available: int = 0
    booked: int = 0
    occupied: int = 0
