from crud.base_crud import CRUDBase
from models.model import Student, Parent, StudentParent
from schemas.student import StudentCreate, StudentUpdate
from sqlalchemy.orm import Session, joinedload
# from core.exceptions import APIException
from fastapi import HTTPException

class StudentCRUD(CRUDBase[Student, StudentCreate]):
    def __init__(self, db: Session):
        super().__init__(Student, db)  # Pass db to the base class
    
    def create(self, obj_in: StudentCreate):
        # Extract parent IDs & relationships from the payload
        parent_relationships = {p.id: p.relationship for p in obj_in.parent_data}
        parent_ids = list(parent_relationships.keys())  

        # Fetch existing parents
        existing_parents = self.db.query(Parent).filter(Parent.id.in_(parent_ids)).all()
        if len(existing_parents) != len(parent_ids):
            raise HTTPException(status_code=400, detail="Some parent IDs do not exist.")

        # Create Student (excluding parent_data)
        student_data = obj_in.model_dump(exclude={"parent_data"})
        student = Student(**student_data)

        # Assign parents through the association table
        associations = [
            StudentParent(parent_id=parent.id, relationship_type=parent_relationships[parent.id])
            for parent in existing_parents
        ]
        
        student.parent_associations.extend(associations)  # ✅ Corrected Relationship Assignment

        self.db.add(student)
        self.db.commit()
        self.db.refresh(student)
        return student

    def update(self, student_id: int, obj_in: StudentUpdate):
        """Update student details and their parent relationships."""
        db_student = self.db.query(Student).filter(Student.id == student_id).first()
        
        if not db_student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Update student fields except parent_data
        update_data = obj_in.model_dump(exclude={"parent_data"}, exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_student, key, value)

        # Handle parent relationships if provided
        if obj_in.parent_data is not None:
            new_parent_relationships = {p.id: p.relationship for p in obj_in.parent_data}
            new_parent_ids = set(new_parent_relationships.keys())

            # Fetch existing parents
            existing_parents = self.db.query(Parent).filter(Parent.id.in_(new_parent_ids)).all()
            if len(existing_parents) != len(new_parent_ids):
                raise HTTPException(status_code=400, detail="Some parent IDs do not exist.")

            # Clear old relationships and set new ones
            self.db.query(StudentParent).filter(StudentParent.student_id == student_id).delete()
            new_associations = [
                StudentParent(parent_id=parent.id, relationship_type=new_parent_relationships[parent.id])
                for parent in existing_parents
            ]
            db_student.parent_associations.extend(new_associations)

        self.db.commit()
        self.db.refresh(db_student)
        return db_student

    def get_by_id(self, student_id: int):
        """Retrieve a student by ID, including parents and relationship details."""
        student = (
            self.db.query(Student)
            .options(joinedload(Student.parent_associations).joinedload(StudentParent.parent))
            .filter(Student.id == student_id)
            .first()
        )
        
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        return student

    def read_students_by_grade(self, grade: int):
        return self.db.query(self.model).filter(self.model.grade == grade).all()


from core.database import get_db
from fastapi import Depends

def get_student_crud(db: Session = Depends(get_db)):
    return StudentCRUD(db)
