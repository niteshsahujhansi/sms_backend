from services.base_service import BaseService
from models.model import Student, Parent, StudentParent, PersonAddress, Address
from schemas.student import StudentCreate, StudentUpdate
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

class StudentService(BaseService[Student, StudentCreate]):

    def __init__(self, tenant_id: str):
        super().__init__(Student, tenant_id)

    def get_by_id(self, student_id: int):
        try:
            with self.sessionmaker() as session:
                student = (
                    session.query(Student)
                    # .options(joinedload(Student.parent_associations).joinedload(StudentParent.parent))
                    # .options(
                    #     joinedload(Student.parent_associations).joinedload(StudentParent.parent),
                    #     joinedload(Student.addresses).joinedload(PersonAddress.address),
                    #     joinedload(Student.medical_details),
                    #     joinedload(Student.transport_details),
                    #     joinedload(Student.student_class_associations)
                    # )
                    .filter(Student.id == student_id)
                    .first()
                )
                
                if not student:
                    raise HTTPException(status_code=404, detail="Student not found")
                
                return student

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def create(self, obj_in: StudentCreate):
        try:
            # Validate email before proceeding
            self.validate_email(obj_in.email)
            
            with self.sessionmaker() as session:
                # Extract parent IDs & relationships from the payload
                parent_relationships = {p.id: p.relationship for p in obj_in.parent_data}
                parent_ids = list(parent_relationships.keys())  

                # Fetch existing parents
                existing_parents = session.query(Parent).filter(Parent.id.in_(parent_ids)).all()
                if len(existing_parents) != len(parent_ids):
                    raise HTTPException(status_code=400, detail="Some parent IDs do not exist.")

                # Create Student (excluding parent_data and address_data)
                student_data = obj_in.model_dump(exclude={"parent_data", "address_data"})
                student = Student(**student_data)

                # Assign parents through the association table
                associations = [
                    StudentParent(parent_id=parent.id, relationship_type=parent_relationships[parent.id])
                    for parent in existing_parents
                ]
                student.parent_associations.extend(associations)

                # Handle Addresses
                addresses = []
                if obj_in.address_data:
                    for address_entry in obj_in.address_data:
                        address_details = address_entry.address

                        # Check if address already exists
                        address = session.query(Address).filter_by(
                            house_no=address_details.house_no,
                            street_address=address_details.street_address,
                            city=address_details.city,
                            state=address_details.state,
                            zip_code=address_details.zip_code,
                            country=address_details.country
                        ).first()

                        if not address:
                            address_data = address_details.model_dump()
                            address = Address(**address_data)
                            session.add(address)
                            session.flush()

                        # Create StudentAddress relationship
                        student_address = PersonAddress(
                            student=student,
                            address=address,
                            address_type=address_entry.address_type
                        )
                        addresses.append(student_address)

                student.addresses.extend(addresses)

                session.add(student)
                session.commit()
                session.refresh(student)

                # # Reload the student with eager loading
                # student = (
                #     session.query(Student)
                #     # .options(
                #     #     selectinload(Student.parent_associations).selectinload(StudentParent.parent),
                #     #     selectinload(Student.addresses).selectinload(PersonAddress.address),
                #     #     selectinload(Student.medical_details),
                #     #     selectinload(Student.transport_details),
                #     #     # selectinload(Student.student_class_associations)
                #     # )
                #     .filter(Student.id == student.id)
                #     .first()
                # )

                return student

        except IntegrityError:
            raise HTTPException(status_code=400, detail="Database integrity error.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def update(self, student_id: int, obj_in: StudentUpdate):
        try:
            with self.sessionmaker() as session:
                db_student = session.query(Student).filter(Student.id == student_id).first()
                
                if not db_student:
                    raise HTTPException(status_code=404, detail="Student not found")

                # Get only the fields that are being updated
                update_data = obj_in.model_dump(exclude={"parent_data"}, exclude_unset=True)
                
                # # If email is being updated, validate it
                # if "email" in update_data:
                #     self.validate_email(update_data["email"])

                # Update student fields except parent_data
                for key, value in update_data.items():
                    setattr(db_student, key, value)

                # Handle parent relationships if provided
                if obj_in.parent_data is not None:
                    new_parent_relationships = {p.id: p.relationship for p in obj_in.parent_data}
                    new_parent_ids = set(new_parent_relationships.keys())

                    # Fetch existing parents
                    existing_parents = session.query(Parent).filter(Parent.id.in_(new_parent_ids)).all()
                    if len(existing_parents) != len(new_parent_ids):
                        raise HTTPException(status_code=400, detail="Some parent IDs do not exist.")

                    # Clear old relationships and set new ones
                    session.query(StudentParent).filter(StudentParent.student_id == student_id).delete()
                    new_associations = [
                        StudentParent(parent_id=parent.id, relationship_type=new_parent_relationships[parent.id])
                        for parent in existing_parents
                    ]
                    db_student.parent_associations.extend(new_associations)

                session.commit()
                session.refresh(db_student)
                return db_student

        except IntegrityError:
            raise HTTPException(status_code=400, detail="Database integrity error.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) 