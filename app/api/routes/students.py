from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.student import StudentCreate, StudentUpdate, StudentResponse, StudentResponseMessage
from services.student_service import StudentService
from api.dependencies import require_roles
from schemas.common_schemas import UserToken

router = APIRouter()

@router.get("/", response_model=list[StudentResponse])
def read_students(current_user: UserToken = Depends(require_roles("admin", "teacher"))):
    student_service = StudentService(current_user.tenant_id)
    return student_service.get_all()

@router.get("/{student_id}", response_model=StudentResponse)
def read_student(student_id: int, current_user: UserToken = Depends(require_roles("admin", "teacher"))):
    student_service = StudentService(current_user.tenant_id)
    student = student_service.get_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# @router.post("/", response_model=StudentResponse)
@router.post("/", response_model=StudentResponseMessage)
def create_new_student(student: StudentCreate, current_user: UserToken = Depends(require_roles("admin", "teacher"))):
    student_service = StudentService(current_user.tenant_id)
    student = student_service.create(student)
    return {"id":student.id, "message": "Student created successfully"}

# @router.put("/{student_id}", response_model=StudentResponse)
@router.put("/{student_id}", response_model=StudentResponseMessage)
def update_existing_student(student_id: int, student: StudentUpdate, current_user: UserToken = Depends(require_roles("admin", "teacher"))):
    student_service = StudentService(current_user.tenant_id)
    updated_student = student_service.update(student_id, student)
    if not updated_student:
        raise HTTPException(status_code=404, detail="Student not found")
    # return updated_student
    return {"id":updated_student.id, "message": "Student updated successfully"}

@router.delete("/{student_id}")
def delete_existing_student(student_id: int, current_user: UserToken = Depends(require_roles("admin", "teacher"))):
    student_service = StudentService(current_user.tenant_id)
    deleted_student = student_service.delete(student_id)
    if not deleted_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}
