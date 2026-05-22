from sqlalchemy import Column, BigInteger, String, SmallInteger, DateTime, Text, func
from app.db.database import Base


class CleaningTask(Base):
    __tablename__ = "cleaning_tasks"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="工单ID")
    room_number = Column(BigInteger, nullable=False, comment="房间号")
    booking_id = Column(BigInteger, comment="关联订单ID")
    status = Column(SmallInteger, default=0, comment="状态: 0-待清洁, 1-清洁中, 2-已完成")
    assignee = Column(String(50), comment="保洁人员")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    completed_at = Column(DateTime, comment="完成时间")
    remark = Column(String(500), comment="备注")
