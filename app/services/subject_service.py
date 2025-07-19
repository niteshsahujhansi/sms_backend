from typing import List
from uuid import UUID
from models.model import Subject, SubjectTeacher
from schemas.class_subject_schemas import SubjectCreate, SubjectTeacherCreate
from services.base_service import BaseService
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

class SubjectService(BaseService[Subject, SubjectCreate]):
    """
    Service layer for Subject entity and its teacher associations, with multi-tenancy support.
    Inherits CRUD from BaseService.
    """
    def __init__(self, tenant_id: str):
        super().__init__(Subject, tenant_id)

    def assign_teachers(self, subject_id: UUID, teachers: List[SubjectTeacherCreate]) -> List[SubjectTeacher]:
        """
        Assign teachers to a subject. Avoids duplicates. Returns all SubjectTeacher associations for the subject.
        """
        try:
            with self.sessionmaker() as session:
                subject = session.query(Subject).filter(Subject.id == subject_id).first()
                if not subject:
                    raise HTTPException(status_code=404, detail="Subject not found")
                for teacher_in in teachers:
                    exists = session.query(SubjectTeacher).filter(
                        SubjectTeacher.subject_id == subject_id,
                        SubjectTeacher.teacher_id == teacher_in.teacher_id
                    ).first()
                    if not exists:
                        assoc = SubjectTeacher(
                            subject_id=subject_id,
                            teacher_id=teacher_in.teacher_id,
                            assigned_date=teacher_in.assigned_date,
                            is_primary=teacher_in.is_primary,
                            is_active=teacher_in.is_active
                        )
                        session.add(assoc)
                session.commit()
                return session.query(SubjectTeacher).filter(SubjectTeacher.subject_id == subject_id).all()
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Database integrity error.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def remove_teacher(self, subject_id: UUID, teacher_id: UUID) -> bool:
        """
        Remove a teacher from a subject. Returns True if removed, False if not found.
        """
        try:
            with self.sessionmaker() as session:
                assoc = session.query(SubjectTeacher).filter(
                    SubjectTeacher.subject_id == subject_id,
                    SubjectTeacher.teacher_id == teacher_id
                ).first()
                if not assoc:
                    return False
                session.delete(assoc)
                session.commit()
                return True
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) 