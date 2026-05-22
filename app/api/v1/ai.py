import json
from pydantic import BaseModel
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.database import get_db
from app.crud.crud_room import get_all
from app.service.ai_service import chat

router = APIRouter(prefix="/api/ai", tags=["AI 智能管家"])

class ChatRequest(BaseModel):
    messages: List[dict]

class ChatResponse(BaseModel):
    content: str


@router.post("/chat")
async def ai_chat(req: ChatRequest, db: AsyncSession = Depends(get_db)):
    """AI 聊天（自动注入真实房间数据作为上下文）"""
    # 1. 查数据库获取真实房间数据
    rooms = await get_all(db)
    room_list = [
        {"room_number": r.room_number, "type": r.type, "price": float(r.price), "status": "空闲" if r.status == 0 else "已预订"}
        for r in rooms
    ]
    room_context = json.dumps(room_list, ensure_ascii=False, indent=2)

    # 2. 调用 AI（带房间数据上下文）
    content = await chat(req.messages, room_context)
    return {"code": 200, "content": content}
