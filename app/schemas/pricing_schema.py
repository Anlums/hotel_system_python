from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PriceAnalysisRequest(BaseModel):
    """AI 定价分析请求"""
    pass  # 不需要额外参数，后端会自行采集数据


class RoomTypePriceInfo(BaseModel):
    """单个房型的价格信息+AI建议"""
    room_type: str
    count: int
    available: int
    occupancy_rate: float
    current_price: float
    suggested_price: float
    reason: str


class PriceAnalysisResponse(BaseModel):
    """AI 分析结果"""
    analysis: str  # AI 分析总结
    suggestions: list[RoomTypePriceInfo]


class ApplyPriceRequest(BaseModel):
    """应用建议价格"""
    room_type: str
    new_price: float
    reason: str


class PriceHistoryResponse(BaseModel):
    id: int
    room_type: str
    old_price: float
    new_price: float
    reason: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
