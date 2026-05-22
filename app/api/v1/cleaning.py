from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.service import cleaning_service
from app.schemas.cleaning_schema import CleaningTaskResponse

router = APIRouter(prefix="/api/cleaning", tags=["保洁管理"])


@router.get("/list")
async def list_tasks(db: AsyncSession = Depends(get_db)):
    tasks = await cleaning_service.list_all(db)
    return {"code": 200, "data": [CleaningTaskResponse.model_validate(t) for t in tasks]}


@router.get("/pending")
async def pending_tasks(db: AsyncSession = Depends(get_db)):
    tasks = await cleaning_service.list_pending(db)
    return {"code": 200, "data": [CleaningTaskResponse.model_validate(t) for t in tasks]}


@router.put("/assign")
async def assign_task(task_id: int, assignee: str, db: AsyncSession = Depends(get_db)):
    try:
        task = await cleaning_service.assign_task(db, task_id, assignee)
        await db.commit()
        return {"code": 200, "msg": f"工单已分配给 {assignee}"}
    except ValueError as e:
        return {"code": 500, "msg": str(e)}


@router.put("/complete")
async def complete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    try:
        task = await cleaning_service.complete_task(db, task_id)
        await db.commit()
        return {"code": 200, "msg": f"房间 {task.room_number} 已清洁完成，可重新入住"}
    except ValueError as e:
        return {"code": 500, "msg": str(e)}
