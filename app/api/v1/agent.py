from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from langchain_core.messages import HumanMessage, AIMessage

from app.db.database import get_db
from app.agent.schema import AgentChatRequest, AgentChatResponse
from app.agent.tools import create_hotel_tools
from app.agent.agent import create_hotel_agent

router = APIRouter(prefix="/api/agent", tags=["AI Agent 智能管家"])


@router.post("/chat", response_model=AgentChatResponse)
async def agent_chat(req: AgentChatRequest, db: AsyncSession = Depends(get_db)):
    """AI Agent 聊天：支持多轮对话 + 工具调用（查询房间、下单等）"""
    tools = create_hotel_tools(db)
    agent = create_hotel_agent(tools)

    # 将前端消息转为 LangChain 消息格式
    messages = []
    for msg in req.messages:
        if msg.role == "user":
            messages.append(HumanMessage(content=msg.content))
        elif msg.role == "assistant":
            messages.append(AIMessage(content=msg.content))

    try:
        # 调用 LangGraph Agent，内部自动处理工具调用循环
        result = await agent.ainvoke({"messages": messages})
        await db.commit()

        # 提取最后一条消息作为回复
        last_message = result["messages"][-1]
        content = last_message.content if hasattr(last_message, "content") else str(last_message)
        return AgentChatResponse(code=200, content=content)

    except Exception as e:
        await db.rollback()
        return AgentChatResponse(code=500, content=f"处理失败：{str(e)}")
