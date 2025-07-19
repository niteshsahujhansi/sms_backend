from typing import List, Optional
from uuid import UUID
from models.model import Schedule
from schemas.schedule import ScheduleCreate
from services.base_service import BaseService
from utils.constants import DayOfWeekEnum
from services.class_service import ClassService
from fastapi import HTTPException

class ScheduleService(BaseService[Schedule, ScheduleCreate]):
    """
    Service layer for Schedule entity, with multi-tenancy support.
    Inherits CRUD from BaseService.
    """
    def __init__(self, tenant_id: str):
        super().__init__(Schedule, tenant_id)

    def list(self, class_id: Optional[UUID] = None, day_of_week: Optional[str] = None, teacher_id: Optional[UUID] = None) -> List[Schedule]:
        """List schedule entries, optionally filter by class_id and day_of_week."""
        with self.sessionmaker() as session:
            query = session.query(Schedule)
            if class_id:
                query = query.filter(Schedule.class_id == class_id)
            if day_of_week:
                query = query.filter(Schedule.day_of_week == day_of_week)
            if teacher_id:
                query = query.filter(Schedule.teacher_id == teacher_id)
            return query.all()

    def get_class_timetable(self, class_id: UUID) -> dict:
        """Return a dict of days to sorted list of Schedule objects for the class, or raise 404 if class not found."""
        class_service = ClassService(self.tenant_id)
        klass = class_service.get_by_id(class_id)
        if not klass:
            raise HTTPException(status_code=404, detail="Class not found")
        
        schedules = self.list(class_id=class_id)
        days = [d.value for d in DayOfWeekEnum]
        periods = list(range(1, klass.total_periods + 1))  # Get period range from class configuration
        
        # Initialize timetable with all days and periods
        timetable = {}
        for day in days:
            timetable[day] = {}
            for period in periods:
                timetable[day][str(period)] = None  # None indicates no schedule for this period
        
        # Fill in actual schedule entries
        for sched in schedules:
            if sched.day_of_week in timetable and str(sched.period_number) in timetable[sched.day_of_week]:
                timetable[sched.day_of_week][str(sched.period_number)] = sched
        
        return timetable

    def get_teacher_timetable(self, teacher_id: UUID) -> dict:
        """Return a dict of days to sorted list of Schedule objects for the teacher."""
        schedules = self.list(teacher_id=teacher_id)
        days = [d.value for d in DayOfWeekEnum]
        
        # For teacher timetable, we need to get periods from all classes they teach
        # For now, we'll use a default range, but this could be enhanced to show
        # the actual period ranges for each class they teach
        periods = list(range(1, 9))  # Default 8 periods for teacher view
        
        # Initialize timetable with all days and periods
        timetable = {}
        for day in days:
            timetable[day] = {}
            for period in periods:
                timetable[day][str(period)] = None  # None indicates no schedule for this period
        
        # Fill in actual schedule entries
        for sched in schedules:
            if sched.day_of_week in timetable and str(sched.period_number) in timetable[sched.day_of_week]:
                timetable[sched.day_of_week][str(sched.period_number)] = sched
        
        return timetable

    def create(self, schedule_data: ScheduleCreate) -> Schedule:
        """Create a new schedule entry with period validation."""
        # Validate period number against class configuration
        class_service = ClassService(self.tenant_id)
        klass = class_service.get_by_id(schedule_data.class_id)
        if not klass:
            raise HTTPException(status_code=404, detail="Class not found")
        
        if schedule_data.period_number > klass.total_periods:
            raise HTTPException(
                status_code=400,
                detail=f"Period number {schedule_data.period_number} exceeds the configured total periods ({klass.total_periods}) for this class"
            )
        
        return super().create(schedule_data)

    def update(self, schedule_id: UUID, schedule_data: dict) -> Schedule:
        """Update a schedule entry with period validation."""
        # Get the current schedule to check class_id
        current_schedule = self.get_by_id(schedule_id)
        if not current_schedule:
            raise HTTPException(status_code=404, detail="Schedule not found")
        
        # Validate period number if it's being updated
        if 'period_number' in schedule_data:
            class_service = ClassService(self.tenant_id)
            klass = class_service.get_by_id(current_schedule.class_id)
            if not klass:
                raise HTTPException(status_code=404, detail="Class not found")
            
            if schedule_data['period_number'] > klass.total_periods:
                raise HTTPException(
                    status_code=400,
                    detail=f"Period number {schedule_data['period_number']} exceeds the configured total periods ({klass.total_periods}) for this class"
                )
        
        return super().update(schedule_id, schedule_data) 