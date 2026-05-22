from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.service import member_service
from app.schemas.member_schema import MemberCreate, MemberUpdate, MemberResponse, PointsRequest

router = APIRouter(prefix="/api/members", tags=["会员管理"])


@router.get("/list")
async def list_members(db: AsyncSession = Depends(get_db)):
    members = await member_service.list_members(db)
    return {"code": 200, "data": [MemberResponse.model_validate(m) for m in members]}


@router.get("/search")
async def search_members(keyword: str = Query(""), db: AsyncSession = Depends(get_db)):
    members = await member_service.search_members(db, keyword)
    return {"code": 200, "data": [MemberResponse.model_validate(m) for m in members]}


@router.get("/lookup")
async def lookup_member(phone: str = Query(...), db: AsyncSession = Depends(get_db)):
    """根据手机号快速查询会员"""
    member = await member_service.lookup_by_phone(db, phone)
    if member:
        return {"code": 200, "data": MemberResponse.model_validate(member)}
    return {"code": 404, "msg": "未找到该手机号的会员"}


@router.post("/add")
async def add_member(data: MemberCreate, db: AsyncSession = Depends(get_db)):
    try:
        member = await member_service.add_member(db, data.name, data.phone, data.id_card, data.email)
        await db.commit()
        return {"code": 200, "msg": "注册成功", "data": MemberResponse.model_validate(member)}
    except ValueError as e:
        return {"code": 500, "msg": str(e)}


@router.put("/update")
async def update_member(member_id: int = Query(...), data: MemberUpdate = None, db: AsyncSession = Depends(get_db)):
    try:
        update_data = {k: v for k, v in data.model_dump().items() if v is not None}
        member = await member_service.update_member(db, member_id, update_data)
        await db.commit()
        return {"code": 200, "msg": "已更新", "data": MemberResponse.model_validate(member)}
    except ValueError as e:
        return {"code": 500, "msg": str(e)}


@router.delete("/delete")
async def delete_member(member_id: int = Query(...), db: AsyncSession = Depends(get_db)):
    try:
        await member_service.delete_member(db, member_id)
        await db.commit()
        return {"code": 200, "msg": "已删除"}
    except ValueError as e:
        return {"code": 500, "msg": str(e)}


@router.put("/points")
async def adjust_points(data: PointsRequest, db: AsyncSession = Depends(get_db)):
    try:
        member = await member_service.adjust_points(db, data.member_id, data.points, data.reason)
        await db.commit()
        return {"code": 200, "msg": f"积分调整完成，当前 {member.points} 分", "data": MemberResponse.model_validate(member)}
    except ValueError as e:
        return {"code": 500, "msg": str(e)}
