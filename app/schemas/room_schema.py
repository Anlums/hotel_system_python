from pydantic import BaseModel, field_validator
from decimal import Decimal
from datetime import datetime
from typing import Optional

# Schema（模式/数据模型） 是用于定义数据结构、验证数据格式、序列化/反序列化数据的契约层。
# 在你的项目中，使用的是 Pydantic 库来创建 Schema。
# 数据验证（Data Validation）类型转换（Type Conversion） API 文档生成（Automatic Documentation）
"""
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   前端请求   │ ──────> │  FastAPI     │ ──────> │  Service层  │
│  JSON 数据   │         │  验证 Schema  │         │  业务逻辑   │
└─────────────┘         └──────────────┘         └─────────────┘
                                                        │
                                                        ▼
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│  前端展示    │ <────── │  序列化      │ <────── │  数据库操作  │
│  JSON 数据   │         │  Response    │         │  CRUD       │
└─────────────┘         └──────────────┘         └─────────────┘
Schema 的核心价值：
✅ 数据验证 - 自动验证请求数据的类型和格式
✅ 类型安全 - IDE 智能提示，减少运行时错误
✅ API 文档 - 自动生成 Swagger/OpenAPI 文档
✅ 代码简洁 - 避免手动验证和转换的重复代码
✅ 前后端分离 - 明确定义 API 接口契约
✅ 错误友好 - 提供清晰的验证错误信息
在你的酒店管理系统中，Schema 是连接前端和后端的数据桥梁，确保了数据的安全性和一致性！

"""

class RoomCreate(BaseModel):
    """新增房间"""
    room_number: int
    type: str = "标准间"  # 默认值
    price : Decimal
    # 字段验证器
    @field_validator('room_number')
    @classmethod
    def validate_room_number(cls, v):
        if v < 1 or v > 9999:
            raise ValueError('房间号必须在 1-9999 之间')
        return v
    @field_validator('price')
    @classmethod
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('价格必须大于 0')
        return v


class RoomUpdate(BaseModel):
    """更新房间"""
    room_number: Optional[int] = None
    type: Optional[str] = None
    price: Optional[Decimal] = None
    status: Optional[int] = None


class RoomResponse(BaseModel):
    """返回给前端的房间信息"""
    id: int
    room_number: int
    type: str
    price: Decimal
    status: int
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None

    model_config = {"from_attributes": True}
