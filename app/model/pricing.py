from sqlalchemy import Column, BigInteger, String, DateTime, Numeric, Text, func
from app.db.database import Base


class PriceHistory(Base):
    """调价历史记录"""
    __tablename__ = "price_history"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="记录ID")
    room_type = Column(String(50), nullable=False, comment="房型")
    old_price = Column(Numeric(10, 2), nullable=False, comment="原价")
    new_price = Column(Numeric(10, 2), nullable=False, comment="新价")
    reason = Column(String(500), comment="调价原因(AI分析)")
    created_at = Column(DateTime, server_default=func.now(), comment="调价时间")
