from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.student import StudentCreate, StudentUpdate, StudentResponse, StudentResponseMessage
from crud.student_crud import StudentCRUD
from api.dependencies import require_roles
from schemas.common_schemas import UserToken

router = APIRouter()

@router.get("/", response_model=list[StudentResponse])
def read_students(current_user: UserToken = Depends(require_roles("admin", "teacher"))):
    student_crud = StudentCRUD(current_user.tenant_id)
    return student_crud.get_all()

@router.get("/{student_id}", response_model=StudentResponse)
# def read_student(student_id: UUID, student_crud: StudentCRUD = Depends(get_student_crud)):
def read_student(student_id: int, current_user: UserToken = Depends(require_roles("admin", "teacher"))):
    student_crud = StudentCRUD(current_user.tenant_id)
    student = student_crud.get_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# @router.post("/", response_model=StudentResponse)
@router.post("/", response_model=StudentResponseMessage)
def create_new_student(student: StudentCreate, current_user: UserToken = Depends(require_roles("admin", "teacher"))):
    student_crud = StudentCRUD(current_user.tenant_id)
    student = student_crud.create(student)
    # return student
    return {"id":student.id, "message": "Student created successfully"}

# @router.put("/{student_id}", response_model=StudentResponse)
@router.put("/{student_id}", response_model=StudentResponseMessage)
def update_existing_student(student_id: int, student: StudentUpdate, current_user: UserToken = Depends(require_roles("admin", "teacher"))):
    student_crud = StudentCRUD(current_user.tenant_id)
    updated_student = student_crud.update(student_id, student)
    if not updated_student:
        raise HTTPException(status_code=404, detail="Student not found")
    # return updated_student
    return {"id":updated_student.id, "message": "Student updated successfully"}

@router.delete("/{student_id}")
def delete_existing_student(student_id: int, current_user: UserToken = Depends(require_roles("admin", "teacher"))):
    student_crud = StudentCRUD(current_user.tenant_id)
    deleted_student = student_crud.delete(student_id)
    if not deleted_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}
