from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.service import room_service_service
from app.schemas.room_service_schema import MenuItemCreate, MenuItemResponse, OrderCreate, OrderResponse

router = APIRouter(prefix="/api/room-service", tags=["客房服务"])


# ==================== 菜单 ====================

@router.get("/menu")
async def get_menu(db: AsyncSession = Depends(get_db)):
    items = await room_service_service.list_menu(db)
    return {"code": 200, "data": [MenuItemResponse.model_validate(i) for i in items]}


@router.post("/menu")
async def add_menu(item: MenuItemCreate, db: AsyncSession = Depends(get_db)):
    new_item = await room_service_service.add_menu_item(db, item.name, item.category, item.price)
    await db.commit()
    return {"code": 200, "msg": "已添加", "data": MenuItemResponse.model_validate(new_item)}


@router.delete("/menu/{item_id}")
async def delete_menu(item_id: int, db: AsyncSession = Depends(get_db)):
    try:
        await room_service_service.remove_menu_item(db, item_id)
        await db.commit()
        return {"code": 200, "msg": "已删除"}
    except ValueError as e:
        return {"code": 500, "msg": str(e)}


# ==================== 订单 ====================

@router.get("/orders")
async def get_orders(db: AsyncSession = Depends(get_db)):
    orders = await room_service_service.list_orders(db)
    return {"code": 200, "data": [OrderResponse.model_validate(o) for o in orders]}


@router.get("/pending")
async def get_pending_orders(db: AsyncSession = Depends(get_db)):
    orders = await room_service_service.list_pending_orders(db)
    return {"code": 200, "data": [OrderResponse.model_validate(o) for o in orders]}


@router.post("/order")
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    new_order = await room_service_service.place_order(
        db, order.room_number, order.items,
        total_amount=order.total_amount,
        guest_name=order.guest_name,
        remark=order.remark,
    )
    await db.commit()
    return {"code": 200, "msg": "下单成功", "data": OrderResponse.model_validate(new_order)}


@router.put("/accept/{order_id}")
async def accept_order(order_id: int, db: AsyncSession = Depends(get_db)):
    try:
        order = await room_service_service.accept_order(db, order_id)
        await db.commit()
        return {"code": 200, "msg": f"订单 {order_id} 开始配送"}
    except ValueError as e:
        return {"code": 500, "msg": str(e)}


@router.put("/deliver/{order_id}")
async def deliver_order(order_id: int, db: AsyncSession = Depends(get_db)):
    try:
        order = await room_service_service.deliver_order(db, order_id)
        await db.commit()
        return {"code": 200, "msg": f"订单 {order_id} 已送达"}
    except ValueError as e:
        return {"code": 500, "msg": str(e)}
