from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID
from schemas.class_subject_schemas import (
    ClassCreate, ClassUpdate, ClassResponse, ClassResponseMessage,
    ClassStudentCreate, ClassStudentResponse,
    ClassSubjectCreate, ClassSubjectResponse
)
from services.class_service import ClassService
# from api.dependencies import require_roles

router = APIRouter()

@router.get("/", response_model=List[ClassResponse])
def list_classes():
    service = ClassService(tenant_id="1")
    result = service.get_all()
    return result

@router.get("/{class_id}", response_model=ClassResponse)
def get_class(class_id: UUID):
    service = ClassService(tenant_id="1")
    klass = service.get_by_id(class_id)
    if not klass:
        raise HTTPException(status_code=404, detail="Class not found")
    return klass

@router.post("/", response_model=ClassResponse)
def create_class(class_in: ClassCreate):
    service = ClassService(tenant_id="1")
    klass = service.create(class_in)
    return klass

@router.put("/{class_id}", response_model=ClassResponse)
def update_class(class_id: UUID, class_in: ClassUpdate):
    service = ClassService(tenant_id="1")
    klass = service.update(class_id, class_in)
    if not klass:
        raise HTTPException(status_code=404, detail="Class not found")
    return klass

@router.delete("/{class_id}")
def delete_class(class_id: UUID):
    service = ClassService(tenant_id="1")
    result = service.delete(class_id)
    if not result:
        raise HTTPException(status_code=404, detail="Class not found")
    return {"message": "Class deleted successfully"}

@router.post("/{class_id}/students/", response_model=List[ClassStudentResponse])
def add_students_to_class(class_id: UUID, students: List[ClassStudentCreate]):
    service = ClassService(tenant_id="1")  # Replace with real tenant_id in production
    result = service.add_students(class_id, students)
    return result

@router.delete("/{class_id}/students/{student_id}")
def remove_student_from_class(class_id: UUID, student_id: int):
    service = ClassService(tenant_id="1")
    result = service.remove_student(class_id, student_id)
    if not result:
        raise HTTPException(status_code=404, detail="Student not found in class")
    return {"message": "Student removed from class"}

@router.post("/{class_id}/subjects/", response_model=List[ClassSubjectResponse])
def add_subjects_to_class(class_id: UUID, subjects: List[ClassSubjectCreate]):
    service = ClassService(tenant_id="1")
    result = service.add_subjects(class_id, subjects)
    return result

@router.delete("/{class_id}/subjects/{subject_id}")
def remove_subject_from_class(class_id: UUID, subject_id: UUID):
    service = ClassService(tenant_id="1")
    result = service.remove_subject(class_id, subject_id)
    if not result:
        raise HTTPException(status_code=404, detail="Subject not found in class")
    return {"message": "Subject removed from class"} 