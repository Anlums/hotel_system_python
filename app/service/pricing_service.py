import json
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import crud_pricing
from app.model.pricing import PriceHistory
from app.service.ai_service import chat


async def analyze_pricing(db: AsyncSession) -> dict:
    """
    采集房间数据，调用 DeepSeek AI 分析，返回建议价格。
    返回: {"analysis": "...", "suggestions": [...]}
    """
    rooms = await crud_pricing.get_all_rooms(db)

    # 按房型聚合
    type_map = {}
    for r in rooms:
        t = r.type
        if t not in type_map:
            type_map[t] = {"count": 0, "available": 0, "prices": []}
        type_map[t]["count"] += 1
        type_map[t]["prices"].append(float(r.price))
        if r.status == 0:
            type_map[t]["available"] += 1

    # 构建 AI 输入
    type_stats = []
    for t, v in sorted(type_map.items()):
        avg_price = round(sum(v["prices"]) / len(v["prices"]), 2)
        occupancy = round((1 - v["available"] / v["count"]) * 100, 1)
        type_stats.append(
            f"- {t}: {v['count']}间, 空闲{v['available']}, "
            f"入住率{occupancy}%, 当前均价{avg_price}元"
        )

    prompt = f"""你是一个酒店收益管理专家。请根据以下房型数据，给出最优的动态定价建议。

当前酒店房型数据：
{chr(10).join(type_stats)}

请按以下 JSON 格式回复（不要加任何其他文字）：
{{
  "analysis": "简短的中文分析总结（50字以内）",
  "suggestions": [
    {{
      "room_type": "房型名称",
      "suggested_price": 建议价格(数字),
      "reason": "调价理由（20字以内）"
    }}
  ]
}}

要求：
1. 入住率超过 70% 的房型可适当涨价 10-20%
2. 入住率低于 30% 的房型可适当降价 10-20% 以吸引预订
3. 考虑房型本身的定位（豪华套房/总统套房可定高价）
4. 价格建议要合理，不能低于成本
5. 所有建议价格保留整数"""

    content = await chat([{"role": "user", "content": prompt}])
    # 解析 AI 返回的 JSON
    try:
        # 清理可能的 markdown 包裹
        text = content.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            text = text.rsplit("```", 1)[0]
        result = json.loads(text.strip())
    except json.JSONDecodeError:
        # 如果 AI 返回的不是纯 JSON，尝试从中提取 JSON 块
        import re
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            result = json.loads(match.group())
        else:
            raise ValueError(f"AI 返回格式异常: {content[:200]}")

    # 补充 current_price 信息
    for s in result["suggestions"]:
        if s["room_type"] in type_map:
            prices = type_map[s["room_type"]]["prices"]
            s["current_price"] = round(sum(prices) / len(prices), 2)
            s["count"] = type_map[s["room_type"]]["count"]
            s["available"] = type_map[s["room_type"]]["available"]
            s["occupancy_rate"] = round(
                (1 - s["available"] / s["count"]) * 100, 1
            )
        else:
            s["current_price"] = 0
            s["count"] = 0
            s["available"] = 0
            s["occupancy_rate"] = 0

    return result


async def apply_pricing(db: AsyncSession, room_type: str, new_price: float, reason: str) -> dict:
    """将某个房型的所有房间改为新价格，并记录调价历史"""
    rooms = await crud_pricing.get_rooms_by_type(db, room_type)
    if not rooms:
        raise ValueError(f"没有找到房型 {room_type}")

    old_price = float(rooms[0].price)
    updated_count = 0
    for room in rooms:
        await crud_pricing.update_room_price(db, room.id, new_price)
        updated_count += 1

    # 记录调价历史
    record = PriceHistory(
        room_type=room_type,
        old_price=old_price,
        new_price=new_price,
        reason=reason,
    )
    await crud_pricing.add_price_history(db, record)

    return {
        "room_type": room_type,
        "old_price": old_price,
        "new_price": new_price,
        "updated_count": updated_count,
        "reason": reason,
    }


async def get_price_history(db: AsyncSession, limit: int = 50) -> list[PriceHistory]:
    return await crud_pricing.get_price_history(db, limit)
