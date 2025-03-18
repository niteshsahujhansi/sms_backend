from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.student import StudentCreate, StudentUpdate, StudentResponse
from crud.student_crud import StudentCRUD


router = APIRouter()

# ✅ Dependency injection to get `StudentCRUD` with a fresh session
def get_student_crud(db: Session = Depends(get_db)):
    return StudentCRUD(db)

@router.get("/", response_model=list[StudentResponse])
def read_students(student_crud: StudentCRUD = Depends(get_student_crud)):
    return student_crud.get_all()

@router.get("/{student_id}", response_model=StudentResponse)
# def read_student(student_id: UUID, student_crud: StudentCRUD = Depends(get_student_crud)):
def read_student(student_id: int, student_crud: StudentCRUD = Depends(get_student_crud)):
    student = student_crud.get_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.post("/", response_model=StudentResponse)
def create_new_student(student: StudentCreate, student_crud: StudentCRUD = Depends(get_student_crud)):
    return student_crud.create(student)

@router.put("/{student_id}", response_model=StudentResponse)
def update_existing_student(student_id: int, student: StudentUpdate, student_crud: StudentCRUD = Depends(get_student_crud)):
    updated_student = student_crud.update(student_id, student)
    if not updated_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated_student

@router.delete("/{student_id}")
def delete_existing_student(student_id: int, student_crud: StudentCRUD = Depends(get_student_crud)):
    deleted_student = student_crud.delete(student_id)
    if not deleted_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}
