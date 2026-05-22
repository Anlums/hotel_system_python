from sqlalchemy.ext.asyncio import AsyncSession
from app.model.room_service import ServiceMenuItem, RoomServiceOrder
from app.crud import crud_room_service


# ==================== 菜单 ====================

async def list_menu(db: AsyncSession) -> list[ServiceMenuItem]:
    return await crud_room_service.get_all_menu_items(db)


async def add_menu_item(db: AsyncSession, name: str, category: str, price: float) -> ServiceMenuItem:
    item = ServiceMenuItem(name=name, category=category, price=price, available=1)
    return await crud_room_service.create_menu_item(db, item)


async def remove_menu_item(db: AsyncSession, item_id: int) -> None:
    deleted = await crud_room_service.delete_menu_item(db, item_id)
    if not deleted:
        raise ValueError("菜单项不存在")


# ==================== 订单 ====================

async def list_orders(db: AsyncSession) -> list[RoomServiceOrder]:
    return await crud_room_service.get_all_orders(db)


async def list_pending_orders(db: AsyncSession) -> list[RoomServiceOrder]:
    return await crud_room_service.get_pending_orders(db)


async def place_order(
    db: AsyncSession,
    room_number: int,
    items: str,
    total_amount: float = 0,
    guest_name: str = None,
    remark: str = None,
) -> RoomServiceOrder:
    order = RoomServiceOrder(
        room_number=room_number,
        guest_name=guest_name,
        items=items,
        total_amount=total_amount,
        status=0,  # 待处理
        remark=remark,
    )
    return await crud_room_service.create_order(db, order)


async def accept_order(db: AsyncSession, order_id: int) -> RoomServiceOrder:
    """接单 → 配送中"""
    order = await crud_room_service.get_order_by_id(db, order_id)
    if not order:
        raise ValueError("订单不存在")
    if order.status != 0:
        raise ValueError("只能接单待处理的订单")
    order = await crud_room_service.update_order_status(db, order_id, 1)
    return order


async def deliver_order(db: AsyncSession, order_id: int) -> RoomServiceOrder:
    """配送完成"""
    order = await crud_room_service.update_order_status(db, order_id, 2)
    if not order:
        raise ValueError("订单不存在")
    return order
