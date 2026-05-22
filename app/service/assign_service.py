import json, re
from sqlalchemy.ext.asyncio import AsyncSession
from langchain_core.messages import HumanMessage
from app.crud import crud_room, crud_booking
from app.service.ai_service import chat
from app.model.booking import Booking
from app.agent.tools import create_hotel_tools
from app.agent.agent import create_hotel_agent, RECOMMEND_SYSTEM_PROMPT


async def recommend_rooms(
    db: AsyncSession,
    guest_count: int = 1,
    preferences: str = "",
) -> dict:
    """AI 根据客人需求推荐最优房间"""
    # 1. 获取所有空闲房间
    available = await crud_room.get_available(db)
    if not available:
        return {
            "analysis": "很抱歉，目前没有空闲房间可推荐。",
            "suggestions": [],
        }

    # 2. 构建房间数据
    room_list = []
    for r in available:
        room_list.append(
            f"- 房间号{r.room_number}: {r.type}, ¥{float(r.price)}/晚"
        )

    # 3. 构建 AI 请求
    prompt = f"""你是一个酒店前台排房专家。请根据客人需求和可用房间，推荐最合适的房间。

客人需求：
- 入住人数：{guest_count}人
- 偏好要求：{preferences or '无特殊要求'}

当前可用房间：
{chr(10).join(room_list)}

房型容量参考：
- 标准间：1-2人
- 大床房：1-2人
- 双床房：1-2人
- 商务套房：1-2人
- 豪华套房：2-3人
- 总统套房：2-4人
- 亲子房：2-4人
- 爱情房间：1-2人
- 小床房：1人

请按以下 JSON 格式回复（不要加任何其他文字）：
{{
  "analysis": "简短分析总结（30字以内）",
  "suggestions": [
    {{
      "room_number": 房间号,
      "room_type": "房型",
      "price": 价格(数字),
      "score": 推荐分1-100(数字),
      "reason": "推荐理由（20字以内）"
    }}
  ]
}}

要求：
1. 最多推荐3间房，按推荐优先级排序
2. 房间容量必须满足入住人数
3. 考虑客人偏好（安静=高层/角落，方便=低层/近电梯，商务=带办公区房型）"""

    content = await chat([{"role": "user", "content": prompt}])

    # 4. 解析 AI 返回
    try:
        text = content.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            text = text.rsplit("```", 1)[0]
        result = json.loads(text.strip())
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            result = json.loads(match.group())
        else:
            raise ValueError(f"AI 返回格式异常: {content[:200]}")

    return result


async def recommend_rooms_via_agent(
    db: AsyncSession,
    guest_count: int = 1,
    preferences: str = "",
) -> dict:
    """用 LangChain Agent 根据客人需求推荐最优房间（替代旧版 recommend_rooms）"""
    tools = create_hotel_tools(db)
    agent = create_hotel_agent(tools, system_prompt=RECOMMEND_SYSTEM_PROMPT)

    prompt = f"客人需求：{guest_count}人，偏好：{preferences or '无特殊要求'}"
    result = await agent.ainvoke({"messages": [HumanMessage(content=prompt)]})

    content = result["messages"][-1].content

    # 从 Agent 回复中提取 JSON
    try:
        text = content.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            text = text.rsplit("```", 1)[0]
        result_data = json.loads(text.strip())
        return result_data
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError(f"Agent 返回格式异常: {content[:200]}")


async def quick_book(
    db: AsyncSession,
    room_number: int,
    guest_name: str,
    phone: str,
    check_in_date: str,
    check_out_date: str | None = None,
) -> Booking:
    """根据推荐一键下单"""
    from app.service.booking_service import parse_dt
    from datetime import timedelta

    # 检查房间是否仍可用
    room = await crud_room.get_by_room_number(db, room_number)
    if not room:
        raise ValueError("房间不存在")
    if room.status != 0:
        raise ValueError(f"房间 {room_number} 已被预订")

    check_in = parse_dt(check_in_date)
    if check_out_date:
        check_out = parse_dt(check_out_date)
    else:
        check_out = check_in.replace(hour=12, minute=0, second=0) + timedelta(days=1)

    # 检查日期冲突
    check_out_str = check_out_date or check_out.strftime("%Y-%m-%d %H:%M:%S")
    conflicts = await crud_booking.get_conflicts(db, room_number, check_in_date, check_out_str)
    if conflicts:
        raise ValueError(f"房间 {room_number} 在选定日期内已被预订")

    days = (check_out.date() - check_in.date()).days
    if days <= 0:
        raise ValueError("退房日期必须晚于入住日期")

    total_amount = float(room.price) * days

    booking = Booking(
        room_number=room_number,
        guest_name=guest_name,
        phone=phone,
        check_in_date=check_in,
        check_out_date=check_out,
        total_amount=total_amount,
        status=1,  # 已预约
    )
    created = await crud_booking.create(db, booking)

    # 房间状态改为已预订
    await crud_room.update_status(db, room_number, 1)

    return created
