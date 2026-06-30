from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MemberCreate(BaseModel):
    """新增会员"""
    name: str
    phone: str
    id_card: Optional[str] = None
    email: Optional[str] = None

class MemberUpdate(BaseModel):
    """修改会员"""
    name: Optional[str] = None
    phone: Optional[str] = None
    id_card: Optional[str] = None
    email: Optional[str] = None


class MemberResponse(BaseModel):
    id: int
    name: str
    phone: str
    id_card: Optional[str] = None
    email: Optional[str] = None
    level: int
    points: int
    total_spent: float
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class PointsRequest(BaseModel):
    """积分调整"""
    member_id: int
    points: int  # 正数增加，负数扣除
    reason: str
