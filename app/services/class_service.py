from typing import List
from uuid import UUID
from models.model import Class, ClassStudent, ClassSubject
from schemas.class_subject_schemas import ClassCreate, ClassStudentCreate, ClassSubjectCreate
from services.base_service import BaseService
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

class ClassService(BaseService[Class, ClassCreate]):
    """
    Service layer for Class entity and its associations (students, subjects), with multi-tenancy support.
    Inherits CRUD from BaseService.
    """
    def __init__(self, tenant_id: str):
        super().__init__(Class, tenant_id)

    def add_students(self, class_id: UUID, students: List[ClassStudentCreate]) -> List[ClassStudent]:
        """
        Add students to a class. Avoids duplicates.
        Returns the list of ClassStudent associations for the class.
        """
        try:
            with self.sessionmaker() as session:
                klass = session.query(Class).filter(Class.id == class_id).first()
                if not klass:
                    raise HTTPException(status_code=404, detail="Class not found")
                added = []
                for student_in in students:
                    # Check if association already exists
                    exists = session.query(ClassStudent).filter(
                        ClassStudent.class_id == class_id,
                        ClassStudent.student_id == student_in.student_id
                    ).first()
                    if not exists:
                        assoc = ClassStudent(
                            class_id=class_id,
                            student_id=student_in.student_id,
                            is_active=student_in.is_active,
                            enrollment_date=student_in.enrollment_date
                        )
                        session.add(assoc)
                        added.append(assoc)
                session.commit()
                # Return all associations for this class
                return session.query(ClassStudent).filter(ClassStudent.class_id == class_id).all()
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Database integrity error.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def remove_student(self, class_id: UUID, student_id: int) -> bool:
        """
        Remove a student from a class. Returns True if removed, False if not found.
        """
        try:
            with self.sessionmaker() as session:
                assoc = session.query(ClassStudent).filter(
                    ClassStudent.class_id == class_id,
                    ClassStudent.student_id == student_id
                ).first()
                if not assoc:
                    return False
                session.delete(assoc)
                session.commit()
                return True
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def add_subjects(self, class_id: UUID, subjects: List[ClassSubjectCreate]) -> List[ClassSubject]:
        """
        Add subjects to a class. Avoids duplicates. Returns all ClassSubject associations for the class.
        """
        try:
            with self.sessionmaker() as session:
                klass = session.query(Class).filter(Class.id == class_id).first()
                if not klass:
                    raise HTTPException(status_code=404, detail="Class not found")
                for subject_in in subjects:
                    exists = session.query(ClassSubject).filter(
                        ClassSubject.class_id == class_id,
                        ClassSubject.subject_id == subject_in.subject_id
                    ).first()
                    if not exists:
                        assoc = ClassSubject(
                            class_id=class_id,
                            subject_id=subject_in.subject_id,
                            assigned_date=subject_in.assigned_date,
                            is_optional=subject_in.is_optional,
                            is_active=subject_in.is_active
                        )
                        session.add(assoc)
                session.commit()
                return session.query(ClassSubject).filter(ClassSubject.class_id == class_id).all()
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Database integrity error.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def remove_subject(self, class_id: UUID, subject_id: UUID) -> bool:
        """
        Remove a subject from a class. Returns True if removed, False if not found.
        """
        try:
            with self.sessionmaker() as session:
                assoc = session.query(ClassSubject).filter(
                    ClassSubject.class_id == class_id,
                    ClassSubject.subject_id == subject_id
                ).first()
                if not assoc:
                    return False
                session.delete(assoc)
                session.commit()
                return True
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) 