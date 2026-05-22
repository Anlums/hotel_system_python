from sqlalchemy import Column, BigInteger, String, SmallInteger, DateTime, Text, Numeric, Boolean, func
from app.db.database import Base


class ServiceMenuItem(Base):
    """服务菜单项"""
    __tablename__ = "service_menu"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="ID")
    name = Column(String(100), nullable=False, comment="项目名称")
    category = Column(String(50), nullable=False, comment="分类: 餐饮/日用品/其他")
    price = Column(Numeric(10, 2), nullable=False, default=0, comment="价格")
    available = Column(SmallInteger, default=1, comment="是否可用: 1-是, 0-否")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")


class RoomServiceOrder(Base):
    """客房服务订单"""
    __tablename__ = "room_service_orders"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="订单ID")
    room_number = Column(BigInteger, nullable=False, comment="房间号")
    guest_name = Column(String(50), comment="客人姓名")
    items = Column(Text, nullable=False, comment="订单项目(JSON数组)")
    total_amount = Column(Numeric(10, 2), nullable=False, default=0, comment="总金额")
    status = Column(SmallInteger, default=0, comment="状态: 0-待处理, 1-配送中, 2-已完成, 3-已取消")
    remark = Column(String(500), comment="备注")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    completed_at = Column(DateTime, comment="完成时间")
