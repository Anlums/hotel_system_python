from typing import Optional
from langchain_core.tools import tool
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal

from app.crud import crud_room, crud_booking
from app.model.booking import Booking
from app.agent.tools_rag import create_rag_tools


def create_hotel_tools(db: AsyncSession) -> list:
    """工具工厂：注入 db session，返回酒店业务工具列表"""

    @tool
    async def query_available_rooms(
        room_type: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        guest_count: Optional[int] = None,
    ) -> str:
        """查询当前空闲房间，可按房型、价格范围、入住人数筛选。
        房型容量参考：标准间=2人, 大床房=2人, 双床房=2人, 商务套房=2人,
        豪华套房=3人, 总统套房=4人, 亲子房=4人, 爱情房间=2人, 小床房=1人"""
        rooms = await crud_room.get_available(db)
        if not rooms:
            return "当前没有空闲房间。"

        # 过滤
        results = []
        for r in rooms:
            if room_type and r.type != room_type:
                continue
            price = float(r.price)
            if min_price is not None and price < min_price:
                continue
            if max_price is not None and price > max_price:
                continue
            results.append(r)

        if not results:
            return "没有符合条件的空闲房间。"

        lines = [f"共 {len(results)} 间空闲房间："]
        for r in results:
            lines.append(f"  - 房间 {r.room_number}：{r.type}，¥{float(r.price)}/晚")
        return "\n".join(lines)

    @tool
    async def check_room_availability(
        room_number: int,
        check_in_date: str,
        check_out_date: str,
    ) -> str:
        """检查指定房间在某个日期范围内是否可用。
        传入日期格式为 YYYY-MM-DD 或 YYYY-MM-DD HH:mm:ss"""
        room = await crud_room.get_by_room_number(db, room_number)
        if not room:
            return f"房间 {room_number} 不存在。"

        # 检查状态
        status_map = {0: "空闲", 1: "已预订", 2: "已入住", 3: "清洁中"}
        if room.status != 0:
            return f"房间 {room_number} 当前状态为「{status_map.get(room.status, '未知')}」，不可预订。"

        # 检查日期冲突
        conflicts = await crud_booking.get_conflicts(db, room_number, check_in_date, check_out_date)
        if conflicts:
            return (f"房间 {room_number} 在 {check_in_date} 至 {check_out_date} "
                    f"期间有 {len(conflicts)} 个冲突订单，不可预订。")

        return (f"房间 {room_number}（{room.type}，¥{float(room.price)}/晚）"
                f"在 {check_in_date} 至 {check_out_date} 期间可用。")

    @tool
    async def get_room_details(room_number: int) -> str:
        """获取指定房间的详细信息，包括房型、价格、当前状态"""
        room = await crud_room.get_by_room_number(db, room_number)
        if not room:
            return f"房间 {room_number} 不存在。"
        status_map = {0: "空闲", 1: "已预订", 2: "已入住", 3: "清洁中"}
        return (f"房间 {room.room_number}：{room.type}，¥{float(room.price)}/晚，"
                f"当前状态：{status_map.get(room.status, '未知')}。")

    @tool
    async def create_booking(
        room_number: int,
        guest_name: str,
        phone: str,
        check_in_date: str,
        check_out_date: Optional[str] = None,
    ) -> str:
        """创建酒店订单。需先确认房间可用，再执行下单。
        传入日期格式为 YYYY-MM-DD 或 YYYY-MM-DD HH:mm:ss。
        退房日期不传则默认入住次日中午"""
        from app.service.booking_service import parse_dt
        from datetime import timedelta

        # 检查房间
        room = await crud_room.get_by_room_number(db, room_number)
        if not room:
            return f"房间 {room_number} 不存在。"
        if room.status != 0:
            return f"房间 {room_number} 当前已被预订。"

        # 解析日期
        try:
            check_in = parse_dt(check_in_date)
        except ValueError as e:
            return f"入住日期格式错误：{e}"
        try:
            check_out = parse_dt(check_out_date) if check_out_date else None
        except ValueError as e:
            return f"退房日期格式错误：{e}"

        if check_out is None:
            check_out = check_in.replace(hour=12, minute=0, second=0) + timedelta(days=1)

        if (check_out.date() - check_in.date()).days <= 0:
            return "退房日期必须晚于入住日期。"

        # 检查冲突
        check_out_str = check_out.strftime("%Y-%m-%d %H:%M:%S")
        conflicts = await crud_booking.get_conflicts(db, room_number, check_in_date, check_out_str)
        if conflicts:
            return f"房间 {room_number} 在该日期范围内已被预订。"

        # 创建订单
        days = (check_out.date() - check_in.date()).days
        total_amount = Decimal(str(float(room.price) * days))
        booking = Booking(
            room_number=room_number,
            guest_name=guest_name,
            phone=phone,
            check_in_date=check_in,
            check_out_date=check_out,
            total_amount=total_amount,
            status=1,
        )
        created = await crud_booking.create(db, booking)
        await crud_room.update_status(db, room_number, 1)

        return (f"预订成功！订单号：{created.id}，房间 {room_number}（{room.type}），"
                f"入住：{check_in.strftime('%Y-%m-%d %H:%M')}，"
                f"退房：{check_out.strftime('%Y-%m-%d %H:%M')}，"
                f"共 {days} 晚，合计 ¥{float(total_amount):.2f}")

    @tool
    async def search_bookings(
        guest_name: Optional[str] = None,
        room_number: Optional[int] = None,
        status: Optional[int] = None,
    ) -> str:
        """查询已有订单，可按客人姓名、房间号、订单状态筛选。
        订单状态：1=已预约, 2=已入住, 3=已退房, 4=已取消"""
        results = await crud_booking.search(db, guest_name, room_number, status)
        if not results:
            return "没有找到匹配的订单。"

        status_map = {1: "已预约", 2: "已入住", 3: "已退房", 4: "已取消"}
        lines = [f"共找到 {len(results)} 条订单："]
        for b in results:
            s = status_map.get(b.status, "未知")
            ci = b.check_in_date.strftime("%Y-%m-%d")
            co = b.check_out_date.strftime("%Y-%m-%d")
            lines.append(f"  - 订单#{b.id}：{b.guest_name}，房间{b.room_number}，"
                         f"{ci}~{co}，¥{float(b.total_amount):.2f}，状态：{s}")
        return "\n".join(lines)

    return [
        query_available_rooms,
        check_room_availability,
        get_room_details,
        create_booking,
        search_bookings,
        *create_rag_tools(),  # RAG 知识库检索工具
    ]
