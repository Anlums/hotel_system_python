from sqlalchemy import Column, BigInteger, String, DateTime, SmallInteger
from sqlalchemy.sql import func
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="用户ID")
    username = Column(String(50), unique=True, nullable=False, comment="用户名")
    password_hash = Column(String(200), nullable=False, comment="密码哈希")
    role = Column(String(20), default="admin", comment="角色: admin/superadmin")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
