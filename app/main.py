from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1 import rooms, bookings, ai, cleaning, room_service, pricing, assign, members, payments
from app.db.database import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时自动创建未存在的表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="天玺尊邸酒店管理系统", version="1.0.0", lifespan=lifespan)

app.include_router(rooms.router)
app.include_router(bookings.router)
app.include_router(ai.router)
app.include_router(cleaning.router)
app.include_router(room_service.router)
app.include_router(pricing.router)
app.include_router(assign.router)
app.include_router(members.router)
app.include_router(payments.router)


@app.get("/")
async def root():
    return {"message": "天玺尊邸酒店管理系统 API"}
