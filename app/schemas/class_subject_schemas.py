from pydantic import BaseModel, Field, field_validator, model_validator, ValidationError
from typing import Optional, List, Dict
from uuid import UUID
from datetime import date, datetime, time
from schemas.common_schemas import CamelCaseModel
from schemas.teacher_schemas import TeacherResponse
from schemas.student import StudentResponse

# --- Class Schemas ---

class PeriodTime(BaseModel):
    start_time: str = Field(..., example="09:00", pattern="^\\d{2}:\\d{2}$")
    end_time: str = Field(..., example="09:45", pattern="^\\d{2}:\\d{2}$")

    @field_validator('start_time', 'end_time')
    @classmethod
    def validate_time_format(cls, v):
        from datetime import time
        try:
            time.fromisoformat(v)
        except ValueError:
            raise ValueError('Time must be in HH:MM format')
        return v

class ClassBase(CamelCaseModel):
    name: str
    section: Optional[str] = None
    academic_year: Optional[str] = None
    room_number: Optional[str] = None
    max_students: Optional[int] = None
    total_periods: Optional[int] = Field(default=8, ge=1, le=12, description="Total number of periods per day (1-12)")
    period_times: Optional[Dict[str, PeriodTime]] = None  # Validated period timetable
    description: Optional[str] = None
    is_active: Optional[bool] = True

    @model_validator(mode="after")
    def check_period_times_length(self):
        if self.period_times is not None and self.total_periods is not None:
            if len(self.period_times) != self.total_periods:
                raise ValueError(
                    f"period_times must have exactly {self.total_periods} items, got {len(self.period_times)}"
                )
            # Optional: check keys are consecutive numbers as strings
            expected_keys = {str(i) for i in range(1, self.total_periods + 1)}
            if set(self.period_times.keys()) != expected_keys:
                raise ValueError(
                    f"period_times keys must be {sorted(expected_keys)}, got {sorted(self.period_times.keys())}"
                )
        return self

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Class 1A",
                "section": "A",
                "academic_year": "2024-2025",
                "room_number": "101",
                "max_students": 40,
                "total_periods": 8,
                "period_times": {
                    "1": {"start_time": "09:00", "end_time": "09:45"},
                    "2": {"start_time": "09:50", "end_time": "10:35"},
                    "3": {"start_time": "10:40", "end_time": "11:25"}
                },
                "description": "Primary class section A",
                "is_active": True
            }
        }

class ClassCreate(ClassBase):
    pass

class ClassUpdate(ClassBase):
    pass

class ClassResponse(ClassBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str] = None
    updated_by: Optional[str] = None

    class Config:
        from_attributes = True

class ClassResponseMessage(CamelCaseModel):
    id: UUID
    message: str

# --- Subject Schemas ---

class SubjectBase(CamelCaseModel):
    name: str
    code: Optional[str] = None
    description: Optional[str] = None
    syllabus: Optional[str] = None
    credits: Optional[int] = None
    is_elective: Optional[bool] = False
    subject_type: Optional[str] = None
    max_marks: Optional[int] = None
    department: Optional[str] = None
    language: Optional[str] = None
    is_active: Optional[bool] = True

class SubjectCreate(SubjectBase):
    pass

class SubjectUpdate(SubjectBase):
    pass

class SubjectResponse(SubjectBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str] = None
    updated_by: Optional[str] = None

    class Config:
        from_attributes = True

class SubjectResponseMessage(CamelCaseModel):
    id: UUID
    message: str

# --- ClassStudent Association Schemas ---

class ClassStudentBase(CamelCaseModel):
    class_id: UUID
    student_id: int
    enrollment_date: Optional[date] = None
    is_active: Optional[bool] = True

class ClassStudentCreate(ClassStudentBase):
    pass

class ClassStudentUpdate(CamelCaseModel):
    enrollment_date: Optional[date] = None
    is_active: Optional[bool] = None

class ClassStudentResponse(ClassStudentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    klass: Optional[ClassResponse] = None
    student: Optional[StudentResponse] = None

    class Config:
        from_attributes = True

# --- ClassSubject Association Schemas ---

class ClassSubjectBase(CamelCaseModel):
    class_id: UUID
    subject_id: UUID
    assigned_date: Optional[date] = None
    is_optional: Optional[bool] = False
    is_active: Optional[bool] = True

class ClassSubjectCreate(ClassSubjectBase):
    pass

class ClassSubjectUpdate(CamelCaseModel):
    assigned_date: Optional[date] = None
    is_optional: Optional[bool] = None
    is_active: Optional[bool] = None

class ClassSubjectResponse(ClassSubjectBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    klass: Optional[ClassResponse] = None
    subject: Optional[SubjectResponse] = None

    class Config:
        from_attributes = True

# --- SubjectTeacher Association Schemas ---

class SubjectTeacherBase(CamelCaseModel):
    subject_id: UUID
    teacher_id: UUID
    assigned_date: Optional[date] = None
    is_primary: Optional[bool] = False
    is_active: Optional[bool] = True

class SubjectTeacherCreate(SubjectTeacherBase):
    pass

class SubjectTeacherUpdate(CamelCaseModel):
    assigned_date: Optional[date] = None
    is_primary: Optional[bool] = None
    is_active: Optional[bool] = None

class SubjectTeacherResponse(SubjectTeacherBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    subject: Optional[SubjectResponse] = None
    teacher: Optional[TeacherResponse] = None

    class Config:
        from_attributes = True 