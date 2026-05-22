from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CleaningTaskResponse(BaseModel):
    id: int
    room_number: int
    booking_id: Optional[int] = None
    status: int
    assignee: Optional[str] = None
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    remark: Optional[str] = None

    model_config = {"from_attributes": True}
