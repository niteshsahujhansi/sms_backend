from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from schemas.schedule import ScheduleCreate, ScheduleUpdate, ScheduleResponse
from services.schedule_service import ScheduleService
from api.dependencies import require_roles
from schemas.common_schemas import UserToken
from collections import defaultdict
from utils.constants import DayOfWeekEnum
from models.model import Class
from schemas.schedule import ScheduleGroupedResponse

router = APIRouter()

@router.get("/", response_model=List[ScheduleResponse])
def list_schedules(
    class_id: Optional[UUID] = Query(None),
    day_of_week: Optional[str] = Query(None),
    current_user: UserToken = Depends(require_roles("admin", "teacher"))
):
    service = ScheduleService(current_user.tenant_id)
    schedules = service.list(class_id=class_id, day_of_week=day_of_week)
    return schedules

@router.get("/{schedule_id}", response_model=ScheduleResponse)
def get_schedule(schedule_id: UUID, current_user: UserToken = Depends(require_roles("admin", "teacher"))):
    service = ScheduleService(current_user.tenant_id)
    schedule = service.get_by_id(schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule

@router.post("/", response_model=ScheduleResponse)
def create_schedule(schedule_in: ScheduleCreate, current_user: UserToken = Depends(require_roles("admin"))):
    service = ScheduleService(current_user.tenant_id)
    schedule = service.create(schedule_in)
    return schedule

@router.put("/{schedule_id}", response_model=ScheduleResponse)
def update_schedule(schedule_id: UUID, schedule_in: ScheduleUpdate, current_user: UserToken = Depends(require_roles("admin"))):
    service = ScheduleService(current_user.tenant_id)
    schedule = service.update(schedule_id, schedule_in)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule

@router.delete("/{schedule_id}")
def delete_schedule(schedule_id: UUID, current_user: UserToken = Depends(require_roles("admin"))):
    service = ScheduleService(current_user.tenant_id)
    result = service.delete(schedule_id)
    if not result:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return {"message": "Schedule deleted successfully"}

@router.get("/class/{class_id}/timetable", response_model=ScheduleGroupedResponse)
def get_class_schedule_grouped(
    class_id: UUID,
    current_user: UserToken = Depends(require_roles("admin", "teacher"))
):
    """Get the full schedule for a class, grouped by day and ordered by period. Includes period timings from class config."""
    service = ScheduleService(current_user.tenant_id)
    schedule_map = service.get_class_timetable(class_id)
    # Fetch class to get period_times
    klass = service.class_service.get_by_id(class_id)
    period_times = klass.period_times if klass and klass.period_times else {}
    result = {}
    for day, periods in schedule_map.items():
        result[day] = {}
        for period_num, schedule in periods.items():
            period_time = period_times.get(str(period_num))
            if schedule is not None:
                # Convert to dict and add period_time info
                resp = ScheduleResponse.from_orm(schedule).dict()
                if period_time:
                    resp["start_time"] = period_time.get("start_time")
                    resp["end_time"] = period_time.get("end_time")
                result[day][period_num] = resp
            else:
                # No schedule, but still provide period_time if available
                if period_time:
                    result[day][period_num] = {"start_time": period_time.get("start_time"), "end_time": period_time.get("end_time")}
                else:
                    result[day][period_num] = None
    return ScheduleGroupedResponse(result)

# @router.get("/teacher/{teacher_id}/timetable", response_model=ScheduleGroupedResponse)
def get_teacher_schedule_grouped(
    teacher_id: UUID,
    current_user: UserToken = Depends(require_roles("admin", "teacher"))
):
    """Get the full schedule for a teacher, grouped by day and ordered by period."""
    service = ScheduleService(current_user.tenant_id)
    schedule_map = service.get_teacher_timetable(teacher_id)
    # Convert to response schema - handle None values for empty periods
    result = {}
    for day, periods in schedule_map.items():
        result[day] = {}
        for period_num, schedule in periods.items():
            if schedule is not None:
                result[day][period_num] = ScheduleResponse.from_orm(schedule)
            else:
                result[day][period_num] = None
    return ScheduleGroupedResponse(result) 