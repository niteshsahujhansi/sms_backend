from pydantic import BaseModel, Field, RootModel
from typing import Optional, Dict, List, Union
from uuid import UUID
from datetime import time, datetime
from utils.constants import DayOfWeekEnum

class ScheduleBase(BaseModel):
    class_id: UUID
    day_of_week: DayOfWeekEnum
    period_number: int
    subject_id: UUID
    teacher_id: UUID
    room: Optional[str] = None
    co_teacher_id: Optional[UUID] = None
    substitute_teacher_id: Optional[UUID] = None
    attendance_taken: Optional[bool] = False
    notification_sent: Optional[bool] = False
    online_link: Optional[str] = None

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleUpdate(BaseModel):
    day_of_week: Optional[DayOfWeekEnum] = None
    period_number: Optional[int] = None
    subject_id: Optional[UUID] = None
    teacher_id: Optional[UUID] = None
    room: Optional[str] = None
    co_teacher_id: Optional[UUID] = None
    substitute_teacher_id: Optional[UUID] = None
    attendance_taken: Optional[bool] = None
    notification_sent: Optional[bool] = None
    online_link: Optional[str] = None

class ScheduleResponse(ScheduleBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# New structure: {day: {period_number: ScheduleResponse | None}}
class ScheduleGroupedResponse(RootModel[Dict[str, Dict[str, Optional[ScheduleResponse]]]]):
    pass 