# app/model/booking.py
from sqlalchemy import Column, BigInteger, String, DECIMAL, SmallInteger, DateTime, func
from app.db.database import Base

class Booking(Base):
    __tablename__ = "bookings"  # 对应 MySQL 表名

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="预订ID")
    room_number = Column(BigInteger, nullable=False, comment="房间编号")
    guest_name = Column(String(50), nullable=False, comment="入住人姓名")
    phone = Column(String(20), nullable=False, comment="联系电话")
    check_in_date = Column(DateTime, nullable=False, comment="入住日期")
    check_out_date = Column(DateTime, nullable=False, comment="退房日期")
    total_amount = Column(DECIMAL(10, 2), nullable=False, comment="订单总金额")
    status = Column(SmallInteger, default=1, comment="订单状态: 1-已预约, 2-已入住, 3-已退房, 4-已取消")
    create_time = Column(DateTime, server_default=func.now(), comment="创建时间")

    
