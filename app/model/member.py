from sqlalchemy import Column, BigInteger, String, SmallInteger, DateTime, Numeric, func
from app.db.database import Base


class Member(Base):
    """会员"""
    __tablename__ = "members"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="会员ID")
    name = Column(String(50), nullable=False, comment="姓名")
    phone = Column(String(20), nullable=False, unique=True, comment="手机号")
    id_card = Column(String(18), comment="身份证号")
    email = Column(String(100), comment="邮箱")
    level = Column(SmallInteger, default=0, comment="等级: 0-普通, 1-银卡, 2-金卡, 3-钻石")
    points = Column(BigInteger, default=0, comment="积分")
    total_spent = Column(Numeric(12, 2), default=0, comment="累计消费")
    created_at = Column(DateTime, server_default=func.now(), comment="注册时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
