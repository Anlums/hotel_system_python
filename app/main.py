from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy import select

from app.api.v1 import rooms, bookings, ai, cleaning, room_service, pricing, assign, members, payments, agent, auth
from app.db.database import engine, Base, async_session
from app.model.user import User
from app.core.security import get_password_hash, decode_token
import jwt


# 放行的路径前缀（不需要登录）
PUBLIC_PATHS = (
    "/api/auth/",
    "/assets/",
    "/docs",
    "/openapi.json",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时自动创建未存在的表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 创建默认管理员（如果不存在）
    async with async_session() as db:
        result = await db.execute(select(User).where(User.username == "admin"))
        if not result.scalar_one_or_none():
            db.add(User(username="admin", password_hash=get_password_hash("admin123"), role="admin"))
            await db.commit()
            print("默认管理员已创建: admin / admin123")
    yield


app = FastAPI(title="天玺尊邸酒店管理系统", version="1.0.0", lifespan=lifespan)

# 注册路由
app.include_router(auth.router)
app.include_router(rooms.router)
app.include_router(bookings.router)
app.include_router(ai.router)
app.include_router(cleaning.router)
app.include_router(room_service.router)
app.include_router(pricing.router)
app.include_router(assign.router)
app.include_router(members.router)
app.include_router(payments.router)
app.include_router(agent.router)


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    """JWT 认证中间件：除登录等公开路径外，所有 API 请求需带 token"""
    path = request.url.path

    # 公开路径放行
    if path.startswith(PUBLIC_PATHS):
        return await call_next(request)

    # /api/ 开头的路径需要认证
    if path.startswith("/api/"):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"code": 401, "msg": "未登录"})
        try:
            payload = decode_token(auth_header.split(" ")[1])
            request.state.user = payload
        except jwt.PyJWTError:
            return JSONResponse(status_code=401, content={"code": 401, "msg": "登录已过期，请重新登录"})

    return await call_next(request)


@app.get("/")
async def root():
    return {"message": "天玺尊邸酒店管理系统 API"}
