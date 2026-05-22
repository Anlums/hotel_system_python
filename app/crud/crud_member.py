from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.model.member import Member


async def get_all(db: AsyncSession) -> list[Member]:
    result = await db.execute(select(Member).order_by(Member.id.desc()))
    return list(result.scalars().all())


async def get_by_id(db: AsyncSession, member_id: int) -> Member | None:
    result = await db.execute(select(Member).where(Member.id == member_id))
    return result.scalar_one_or_none()


async def get_by_phone(db: AsyncSession, phone: str) -> Member | None:
    result = await db.execute(select(Member).where(Member.phone == phone))
    return result.scalar_one_or_none()


async def search(db: AsyncSession, keyword: str) -> list[Member]:
    result = await db.execute(
        select(Member).where(
            or_(Member.name.like(f"%{keyword}%"), Member.phone.like(f"%{keyword}%"))
        ).order_by(Member.id.desc())
    )
    return list(result.scalars().all())


async def create(db: AsyncSession, member: Member) -> Member:
    db.add(member)
    await db.flush()
    await db.refresh(member)
    return member


async def update(db: AsyncSession, member_id: int, data: dict) -> Member | None:
    member = await get_by_id(db, member_id)
    if not member:
        return None
    for key, value in data.items():
        if value is not None:
            setattr(member, key, value)
    await db.flush()
    await db.refresh(member)
    return member


async def delete(db: AsyncSession, member_id: int) -> bool:
    member = await get_by_id(db, member_id)
    if not member:
        return False
    await db.delete(member)
    return True


async def update_points(db: AsyncSession, member_id: int, points: int) -> Member | None:
    """调整积分（正加负减），并自动更新会员等级"""
    member = await get_by_id(db, member_id)
    if not member:
        return None
    member.points = max(0, member.points + points)
    # 自动升级：积分 >= 10000 → 钻石, >= 5000 → 金卡, >= 1000 → 银卡
    if member.points >= 10000:
        member.level = 3
    elif member.points >= 5000:
        member.level = 2
    elif member.points >= 1000:
        member.level = 1
    await db.flush()
    await db.refresh(member)
    return member
