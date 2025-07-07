from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import and_
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from services.base_service import BaseService
from models.model import Teacher, PersonAddress, Address
from schemas.teacher_schemas import TeacherCreate, TeacherUpdate
from pydantic import EmailStr

class TeacherService(BaseService[Teacher, TeacherCreate]):
    def __init__(self, tenant_id: str):
        super().__init__(Teacher, tenant_id)

    def create(self, obj_in: TeacherCreate):
        try:
            # Validate email before proceeding
            self.validate_email(obj_in.email)
            
            with self.sessionmaker() as session:
                # Extract addresses from input
                address_data = obj_in.addresses
                
                new_addresses = []
                teacher_address_associations = []

                if address_data:
                    for addr_data in address_data:
                        address_type = addr_data.address_type
                        addr = addr_data.address

                        # Check if the same address exists
                        existing_address = (
                            session.query(Address)
                            .filter(
                                Address.house_no == addr.house_no,
                                Address.street_address == addr.street_address,
                                Address.landmark == addr.landmark,
                                Address.city == addr.city,
                                Address.state == addr.state,
                                Address.zip_code == addr.zip_code,
                                Address.country == addr.country,
                            )
                            .first()
                        )

                        if existing_address:
                            address = existing_address
                        else:
                            address = Address(**addr.model_dump())
                            session.add(address)
                            new_addresses.append(address)

                        session.flush()  # Make sure address has an ID

                        # Create PersonAddress entry
                        teacher_address = PersonAddress(
                            address_id=address.id,
                            address_type=address_type,
                        )
                        teacher_address_associations.append(teacher_address)

                # Create teacher without addresses
                teacher = Teacher(**obj_in.model_dump(exclude={"addresses"}))
                session.add(teacher)
                session.flush()

                # Link addresses
                for ta in teacher_address_associations:
                    ta.teacher_id = teacher.id
                    session.add(ta)

                session.commit()    
                session.refresh(teacher)
                return teacher

        # except IntegrityError:
        #     raise HTTPException(status_code=400, detail="Database integrity error.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def update(self, teacher_id: str, obj_in: TeacherUpdate):
        try:
            with self.sessionmaker() as session:
                teacher = session.query(Teacher).filter(Teacher.id == teacher_id).first()
                if not teacher:
                    raise HTTPException(status_code=404, detail="Teacher not found")

                # Get only the fields that are being updated
                update_data = obj_in.model_dump(exclude_unset=True, exclude={"addresses"})
                
                # If email is being updated, validate it
                if "email" in update_data:
                    self.validate_email(update_data["email"], exclude_id=teacher_id)

                # Update teacher fields except addresses
                for key, value in update_data.items():
                    setattr(teacher, key, value)

                # Handle address updates if present
                if obj_in.addresses:
                    # existing_addresses keyed by address_type for quick lookup
                    existing_addresses = {pa.address_type: pa.address for pa in teacher.addresses}

                    for addr_data in obj_in.addresses:
                        address_type = addr_data.address_type
                        new_address_data = addr_data.address

                        if address_type in existing_addresses:
                            existing_address = existing_addresses[address_type]
                            for field, new_value in new_address_data.model_dump().items():
                                setattr(existing_address, field, new_value)
                        else:
                            # Create new address and association
                            new_address = Address(**new_address_data.model_dump())
                            session.add(new_address)
                            session.flush()  # Get new_address.id

                            new_ta = PersonAddress(teacher_id=teacher.id, address_id=new_address.id, address_type=address_type)
                            session.add(new_ta)

                session.commit()
                session.refresh(teacher)
                return teacher

        except IntegrityError:
            raise HTTPException(status_code=400, detail="Database integrity error.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def create_teacher(self, db: Session, obj_in: TeacherCreate) -> Teacher:
        db_obj = Teacher(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def soft_delete_teacher(self, db: Session, teacher_id: str) -> Optional[Teacher]:
        db_obj = self.get(db=db, id=teacher_id)
        if not db_obj:
            return None
        db_obj.is_deleted = True
        db_obj.is_active = False
        db.commit()
        db.refresh(db_obj)
        return db_obj 