from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID
from schemas.class_subject_schemas import (
    SubjectCreate, SubjectUpdate, SubjectResponse, SubjectResponseMessage,
    SubjectTeacherCreate, SubjectTeacherResponse
)
from services.subject_service import SubjectService
# from api.dependencies import require_roles

router = APIRouter()

@router.get("/", response_model=List[SubjectResponse])
def list_subjects():
    service = SubjectService(tenant_id="1")
    result = service.get_all()
    return result

@router.get("/{subject_id}", response_model=SubjectResponse)
def get_subject(subject_id: UUID):
    service = SubjectService(tenant_id="1")
    subject = service.get_by_id(subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject

@router.post("/", response_model=SubjectResponseMessage)
def create_subject(subject_in: SubjectCreate):
    service = SubjectService(tenant_id="1")
    subject = service.create(subject_in)
    return {"id": subject.id, "message": "Subject created successfully"}

@router.put("/{subject_id}", response_model=SubjectResponse)
def update_subject(subject_id: UUID, subject_in: SubjectUpdate):
    service = SubjectService(tenant_id="1")
    subject = service.update(subject_id, subject_in)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject

@router.delete("/{subject_id}")
def delete_subject(subject_id: UUID):
    service = SubjectService(tenant_id="1")
    result = service.delete(subject_id)
    if not result:
        raise HTTPException(status_code=404, detail="Subject not found")
    return {"message": "Subject deleted successfully"}

@router.post("/{subject_id}/teachers/", response_model=List[SubjectTeacherResponse])
def assign_teachers_to_subject(subject_id: UUID, teachers: List[SubjectTeacherCreate]):
    service = SubjectService(tenant_id="1")
    result = service.assign_teachers(subject_id, teachers)
    return result

@router.delete("/{subject_id}/teachers/{teacher_id}")
def remove_teacher_from_subject(subject_id: UUID, teacher_id: UUID):
    service = SubjectService(tenant_id="1")
    result = service.remove_teacher(subject_id, teacher_id)
    if not result:
        raise HTTPException(status_code=404, detail="Teacher not found for subject")
    return {"message": "Teacher removed from subject"} 