from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MenuItemCreate(BaseModel):
    """新增菜单项"""
    name: str
    category: str
    price: float


class MenuItemResponse(BaseModel):
    id: int
    name: str
    category: str
    price: float
    available: int
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class OrderCreate(BaseModel):
    """创建客房服务订单"""
    room_number: int
    guest_name: Optional[str] = None
    items: str  # JSON 数组字符串, e.g. [{"name":"咖啡","price":25,"qty":2}]
    total_amount: float = 0
    remark: Optional[str] = None


class OrderResponse(BaseModel):
    id: int
    room_number: int
    guest_name: Optional[str] = None
    items: str
    total_amount: float
    status: int
    remark: Optional[str] = None
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
