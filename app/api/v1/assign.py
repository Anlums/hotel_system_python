from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.service import assign_service

router = APIRouter(prefix="/api/assign", tags=["AI 智能排房"])


@router.get("/recommend")
async def recommend(
    guest_count: int = Query(1, ge=1, le=10, description="入住人数"),
    preferences: str = Query("", description="偏好要求，如: 安静、高层、商务"),
    db: AsyncSession = Depends(get_db),
):
    """AI 根据客人需求推荐最优房间"""
    try:
        result = await assign_service.recommend_rooms(db, guest_count, preferences)
        return {"code": 200, "data": result}
    except Exception as e:
        return {"code": 500, "msg": f"推荐失败: {str(e)}"}


@router.post("/book")
async def quick_book(
    room_number: int = Query(..., description="房间号"),
    guest_name: str = Query(..., description="客人姓名"),
    phone: str = Query(..., description="手机号"),
    check_in_date: str = Query(..., description="入住日期 yyyy-MM-dd HH:mm:ss"),
    check_out_date: str = Query(None, description="退房日期 yyyy-MM-dd HH:mm:ss，不填默认+1天"),
    db: AsyncSession = Depends(get_db),
):
    """根据推荐一键下单"""
    try:
        booking = await assign_service.quick_book(
            db, room_number, guest_name, phone, check_in_date, check_out_date
        )
        await db.commit()
        from app.schemas.booking_schema import BookingResponse
        return {
            "code": 200,
            "msg": f"预订成功，房间 {room_number} 已为您保留",
            "data": BookingResponse.model_validate(booking),
        }
    except ValueError as e:
        return {"code": 500, "msg": str(e)}
