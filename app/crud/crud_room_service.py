from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.model.room_service import ServiceMenuItem, RoomServiceOrder
from datetime import datetime
import json


# ==================== 菜单管理 ====================

async def get_all_menu_items(db: AsyncSession) -> list[ServiceMenuItem]:
    result = await db.execute(
        select(ServiceMenuItem).order_by(ServiceMenuItem.category, ServiceMenuItem.id)
    )
    return list(result.scalars().all())


async def get_menu_item_by_id(db: AsyncSession, item_id: int) -> ServiceMenuItem | None:
    result = await db.execute(select(ServiceMenuItem).where(ServiceMenuItem.id == item_id))
    return result.scalar_one_or_none()


async def create_menu_item(db: AsyncSession, item: ServiceMenuItem) -> ServiceMenuItem:
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return item


async def delete_menu_item(db: AsyncSession, item_id: int) -> bool:
    result = await db.execute(select(ServiceMenuItem).where(ServiceMenuItem.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        return False
    await db.delete(item)
    return True


# ==================== 订单管理 ====================

async def get_all_orders(db: AsyncSession) -> list[RoomServiceOrder]:
    result = await db.execute(
        select(RoomServiceOrder).order_by(RoomServiceOrder.id.desc())
    )
    return list(result.scalars().all())


async def get_pending_orders(db: AsyncSession) -> list[RoomServiceOrder]:
    """获取待处理和配送中的订单"""
    result = await db.execute(
        select(RoomServiceOrder)
        .where(RoomServiceOrder.status.in_([0, 1]))
        .order_by(RoomServiceOrder.id.desc())
    )
    return list(result.scalars().all())


async def get_order_by_id(db: AsyncSession, order_id: int) -> RoomServiceOrder | None:
    result = await db.execute(select(RoomServiceOrder).where(RoomServiceOrder.id == order_id))
    return result.scalar_one_or_none()


async def create_order(db: AsyncSession, order: RoomServiceOrder) -> RoomServiceOrder:
    db.add(order)
    await db.flush()
    await db.refresh(order)
    return order


async def update_order_status(db: AsyncSession, order_id: int, status: int) -> RoomServiceOrder | None:
    order = await get_order_by_id(db, order_id)
    if not order:
        return None
    order.status = status
    if status in (2, 3):  # 已完成或已取消
        order.completed_at = datetime.now()
    await db.flush()
    await db.refresh(order)
    return order
