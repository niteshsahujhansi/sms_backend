from sqlalchemy.orm import Session, selectinload
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from crud.base_crud import CRUDBase
from models.model import Parent, PersonAddress, Address
from schemas.parent import ParentCreate, ParentUpdate
from typing import List

class ParentCRUD(CRUDBase[Parent, ParentCreate]):
    def __init__(self, tenant_id: str):
        super().__init__(Parent, tenant_id)

    def create(self, obj_in: ParentCreate):
        try:
            with self.sessionmaker() as session:
                # Extract addresses from input
                address_data = obj_in.addresses
                
                new_addresses = []
                parent_address_associations = []

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
                        parent_address = PersonAddress(
                            address_id=address.id,
                            address_type=address_type,
                        )
                        parent_address_associations.append(parent_address)

                # Create parent without addresses
                parent = Parent(**obj_in.model_dump(exclude={"addresses"}))
                session.add(parent)
                session.flush()

                # Link addresses
                for pa in parent_address_associations:
                    pa.parent_id = parent.id
                    session.add(pa)

                session.commit()    
                session.refresh(parent)
                return parent

        except IntegrityError:
            raise HTTPException(status_code=400, detail="Database integrity error.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    def update(self, parent_id: int, obj_in: ParentUpdate):
        try:
            with self.sessionmaker() as session:
                parent = session.query(Parent).filter(Parent.id == parent_id).first()
                if not parent:
                    raise HTTPException(status_code=404, detail="Parent not found")

                # Update parent fields except addresses
                update_data = obj_in.model_dump(exclude_unset=True, exclude={"addresses"})
                for key, value in update_data.items():
                    setattr(parent, key, value)

                # Handle address updates if present
                if obj_in.addresses:
                    # existing_addresses keyed by address_type for quick lookup
                    existing_addresses = {pa.address_type: pa.address for pa in parent.addresses}

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

                            new_pa = PersonAddress(parent_id=parent.id, address_id=new_address.id, address_type=address_type)
                            session.add(new_pa)

                session.commit()
                session.refresh(parent)
                return parent

        except IntegrityError:
            raise HTTPException(status_code=400, detail="Database integrity error.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
