from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.service import pricing_service
from app.schemas.pricing_schema import PriceAnalysisResponse, ApplyPriceRequest, PriceHistoryResponse

router = APIRouter(prefix="/api/pricing", tags=["AI 动态定价"])


@router.get("/analyze")
async def analyze(db: AsyncSession = Depends(get_db)):
    """AI 分析当前入住率并给出各房型建议价格"""
    try:
        result = await pricing_service.analyze_pricing(db)
        return {"code": 200, "data": result}
    except Exception as e:
        return {"code": 500, "msg": f"分析失败: {str(e)}"}


@router.post("/apply")
async def apply(req: ApplyPriceRequest, db: AsyncSession = Depends(get_db)):
    """应用某个房型的建议价格"""
    try:
        result = await pricing_service.apply_pricing(db, req.room_type, req.new_price, req.reason)
        await db.commit()
        return {"code": 200, "msg": f"已更新 {result['updated_count']} 间{req.room_type}", "data": result}
    except ValueError as e:
        return {"code": 500, "msg": str(e)}


@router.get("/history")
async def history(limit: int = Query(50, ge=1, le=200), db: AsyncSession = Depends(get_db)):
    """调价历史记录"""
    records = await pricing_service.get_price_history(db, limit)
    return {"code": 200, "data": [PriceHistoryResponse.model_validate(r) for r in records]}
