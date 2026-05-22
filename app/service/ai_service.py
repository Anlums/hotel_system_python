import httpx
from app.core.config import settings

DEFAULT_SYSTEM_PROMPT = "你现在是天玺尊邸酒店的 AI 智能管家，请用专业、尊贵的语气回答问题。你的回答请控制在200字以内。"


def make_system_prompt(room_context: str = "") -> str:
    """根据是否有房间数据，生成对应的 system prompt"""
    if room_context:
        return f"""你现在是天玺尊邸酒店的 AI 智能管家，请用专业、尊贵的语气回答问题。

以下是当前酒店的房间数据（JSON格式），当客人咨询房间推荐时，请基于这些真实数据给出建议，不要编造不存在的房型或价格：
{room_context}

你的回答请控制在200字以内。"""
    return DEFAULT_SYSTEM_PROMPT


async def chat(messages: list[dict], room_context: str = "") -> str:
    """调用 DeepSeek V4 API"""
    headers = {
        "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }
    system_prompt = make_system_prompt(room_context)
    full_messages = [{"role": "system", "content": system_prompt}, *messages]

    payload = {
        "model": settings.DEEPSEEK_MODEL,
        "messages": full_messages,
        "stream": False,
    }

    if "pro" in settings.DEEPSEEK_MODEL or "reasoner" in settings.DEEPSEEK_MODEL:
        payload["thinking"] = {"type": "enabled"}
        payload["reasoning_effort"] = "high"

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(settings.DEEPSEEK_BASE_URL, json=payload, headers=headers)
        if resp.is_success:
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        else:
            return f"AI 服务调用失败: {resp.status_code} {resp.text}"
