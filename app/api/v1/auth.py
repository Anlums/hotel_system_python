from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.db.database import get_db
from app.model.user import User
from app.core.security import verify_password, create_access_token

router = APIRouter(prefix="/api/auth", tags=["认证"])

class AuthLogin(BaseModel):
    username: str
    password: str


@router.post("/login")
async def login(data: AuthLogin, db: AsyncSession = Depends(get_db)):
    """管理员登录，返回 JWT token"""
    from sqlalchemy import select

    result = await db.execute(select(User).where(User.username == data.username))
    user = result.scalar_one_or_none()

    if not user or not verify_password(data.password, user.password_hash):
        return {"code": 401, "msg": "用户名或密码错误"}
    """
    📋 Header = 证件类型说明
    👤 Payload = 你的个人信息
    🔏 Signature = 公安局的防伪印章
    """
    token = create_access_token({"sub": user.username, "role": user.role})
    return {
        "code": 200,
        "data": {
            "token": token,
            "username": user.username,
            "role": user.role,
        },
    }
