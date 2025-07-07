from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.teacher_schemas import TeacherCreate, TeacherUpdate, TeacherResponse, TeacherResponseMessage
from services.teacher_service import TeacherService
from api.dependencies import require_roles
from schemas.common_schemas import UserToken
from pydantic import UUID4

router = APIRouter()

@router.get("/", response_model=list[TeacherResponse])
def read_teachers(
    # current_user: UserToken = Depends(require_roles("admin", "teacher"))
):
    teacher_service = TeacherService(tenant_id="1")  # Fixed tenant_id for testing
    return teacher_service.get_all()

@router.get("/{teacher_id}", response_model=TeacherResponse)
def read_teacher(
    teacher_id: UUID4,
    # current_user: UserToken = Depends(require_roles("admin"))
):
    teacher_service = TeacherService(tenant_id="1")  # Fixed tenant_id for testing
    teacher = teacher_service.get_by_id(teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher

@router.post("/", response_model=TeacherResponseMessage)
def create_teacher(
    teacher: TeacherCreate,
    # current_user: UserToken = Depends(require_roles("admin"))
):
    teacher_service = TeacherService(tenant_id="1")  # Fixed tenant_id for testing
    teacher = teacher_service.create(teacher)
    return {"id": teacher.id, "message": "Teacher created successfully"}

@router.put("/{teacher_id}", response_model=TeacherResponse)
def update_teacher(
    teacher_id: UUID4,
    teacher: TeacherUpdate,
    # current_user: UserToken = Depends(require_roles("admin"))
):
    teacher_service = TeacherService(tenant_id="1")  # Fixed tenant_id for testing
    updated_teacher = teacher_service.update(teacher_id, teacher)
    if not updated_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return updated_teacher

@router.delete("/{teacher_id}")
def delete_teacher(
    teacher_id: UUID4,
    # current_user: UserToken = Depends(require_roles("admin"))
):
    teacher_service = TeacherService(tenant_id="1")  # Fixed tenant_id for testing
    deleted_teacher = teacher_service.delete(teacher_id)
    if not deleted_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return {"message": "Teacher deleted successfully"}
