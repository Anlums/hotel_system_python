# app/model/room.py
from sqlalchemy import Column, BigInteger, String, DECIMAL, SmallInteger, DateTime, func
from app.db.database import Base

class Room(Base):
    __tablename__ = "rooms"  # 对应 MySQL 表名

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="房间ID")
    room_number = Column(BigInteger, nullable=False, unique=True, comment="房间编号")
    type = Column(String(50), nullable=False, comment="房型")
    price = Column(DECIMAL(10, 2), nullable=False, comment="每晚价格")
    status = Column(SmallInteger, default=0, comment="状态: 0-空闲, 1-已预订")
    create_time = Column(DateTime, server_default=func.now(), comment="创建时间")
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
