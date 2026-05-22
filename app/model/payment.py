# app/model/payment.py
from sqlalchemy import Column, BigInteger, String, DECIMAL, DateTime, func, Text
from app.db.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="支付ID")
    booking_id = Column(BigInteger, nullable=False, comment="关联订单ID")
    type = Column(String(20), nullable=False, comment="类型: deposit=押金, payment=房费, refund=退款")
    amount = Column(DECIMAL(10, 2), nullable=False, comment="金额(正数=收入, 负数=支出)")
    method = Column(String(20), default="cash", comment="支付方式: cash/wechat/alipay/card")
    status = Column(String(20), default="completed", comment="状态: completed/refunded")
    remark = Column(Text, nullable=True, comment="备注")
    operator = Column(String(50), default="系统", comment="操作人")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
