from pydantic import BaseModel
from typing import List, Optional


class AgentMessage(BaseModel):
    """前端传来的单条消息"""
    role: str  # "user" | "assistant"
    content: str


class AgentChatRequest(BaseModel):
    """Agent 聊天请求"""
    messages: List[AgentMessage]


class AgentChatResponse(BaseModel):
    """Agent 聊天响应"""
    code: int = 200
    content: str = ""
