from sqlalchemy.ext.asyncio import AsyncSession
from app.model.member import Member
from app.crud import crud_member


async def list_members(db: AsyncSession) -> list[Member]:
    return await crud_member.get_all(db)


async def search_members(db: AsyncSession, keyword: str) -> list[Member]:
    return await crud_member.search(db, keyword)


async def add_member(db: AsyncSession, name: str, phone: str, id_card: str = None, email: str = None) -> Member:
    # 检查手机号是否已注册
    existing = await crud_member.get_by_phone(db, phone)
    if existing:
        raise ValueError(f"手机号 {phone} 已注册为会员: {existing.name}")
    member = Member(name=name, phone=phone, id_card=id_card, email=email, level=0, points=0)
    return await crud_member.create(db, member)


async def update_member(db: AsyncSession, member_id: int, data: dict) -> Member:
    member = await crud_member.update(db, member_id, data)
    if not member:
        raise ValueError("会员不存在")
    return member


async def delete_member(db: AsyncSession, member_id: int) -> None:
    deleted = await crud_member.delete(db, member_id)
    if not deleted:
        raise ValueError("会员不存在")


async def adjust_points(db: AsyncSession, member_id: int, points: int, reason: str) -> Member:
    member = await crud_member.update_points(db, member_id, points)
    if not member:
        raise ValueError("会员不存在")
    return member


async def lookup_by_phone(db: AsyncSession, phone: str) -> Member | None:
    """根据手机号查询会员（供下单时快速查找）"""
    return await crud_member.get_by_phone(db, phone)
