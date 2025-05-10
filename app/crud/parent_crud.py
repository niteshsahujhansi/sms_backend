from sqlalchemy.orm import Session
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
            # Extract addresses from input
            address_data = obj_in.addresses  # List of address objects
            
            new_addresses = []
            linked_addresses = []
            parent_address_associations = []  # To store PersonAddress objects

            if address_data:
                for addr_data in address_data:
                    address_type = addr_data.address_type
                    addr = addr_data.address  # Extract address fields
                    
                    # Check if the same address exists
                    existing_address = (
                        self.session.query(Address)
                        .filter(
                            Address.house_no == addr.house_no,
                            Address.street_address == addr.street_address,
                            Address.landmark == addr.landmark,
                            Address.city == addr.city,
                            Address.state == addr.state,
                            Address.zip_code == addr.zip_code,
                            Address.country == addr.country
                        )
                        .first()
                    )

                    if existing_address:
                        address = existing_address  # Use existing address
                    else:
                        address = Address(**addr.model_dump())
                        self.session.add(address)
                        new_addresses.append(address)

                    self.session.flush()  # Ensure new addresses get an ID
                    
                    # Create PersonAddress entry
                    parent_address = PersonAddress(
                        address_id=address.id,  # ✅ Corrected: Use address_id, not address
                        address_type=address_type
                    )
                    parent_address_associations.append(parent_address)

            # Create Parent (excluding addresses)
            parent = Parent(**obj_in.model_dump(exclude={"addresses"}))

            # Commit parent first to get the ID
            self.session.add(parent)
            self.session.flush()

            # Link addresses to the parent
            for pa in parent_address_associations:
                pa.parent_id = parent.id  # Assign parent ID after creation
                self.session.add(pa)

            self.session.commit()
            self.session.refresh(parent)
            return parent

        # except IntegrityError:
        #     self.session.rollback()
        #     raise HTTPException(status_code=400, detail="Database integrity error.")
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def update(self, parent_id: int, obj_in: ParentUpdate):
        try:
            parent = self.session.query(Parent).filter(Parent.id == parent_id).first()
            if not parent:
                raise HTTPException(status_code=404, detail="Parent not found")

            # Update parent details (excluding addresses)
            update_data = obj_in.model_dump(exclude_unset=True, exclude={"addresses"})
            for key, value in update_data.items():
                setattr(parent, key, value)

            # Handle address updates
            if obj_in.addresses:
                existing_addresses = {pa.address_type: pa.address for pa in parent.addresses}  # Key by address_type
                
                for addr_data in obj_in.addresses:
                    address_type = addr_data.address_type  # "Current" or "Permanent"
                    new_address_data = addr_data.address

                    if address_type in existing_addresses:
                        # Update the existing address (Modify fields)
                        existing_address = existing_addresses[address_type]
                        for field, new_value in new_address_data.model_dump().items():
                            setattr(existing_address, field, new_value)

                    else:
                        # If the address type doesn't exist, create a new one
                        new_address = Address(**new_address_data.model_dump())
                        self.session.add(new_address)
                        self.session.flush()  # Ensure new address gets an ID

                        # Link the new address to the parent
                        new_pa = PersonAddress(parent_id=parent.id, address_id=new_address.id, address_type=address_type)
                        self.session.add(new_pa)

            self.session.commit()
            self.session.refresh(parent)
            return parent

        except IntegrityError:
            self.session.rollback()
            raise HTTPException(status_code=400, detail="Database integrity error.")
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def update_without_address(self, parent_id: int, obj_in: ParentUpdate):
        try:
            parent = self.session.query(Parent).filter(Parent.id == parent_id).first()
            if not parent:
                raise HTTPException(status_code=404, detail="Parent not found")

            # Update parent details
            update_data = obj_in.model_dump(exclude_unset=True, exclude={"addresses"})
            for key, value in update_data.items():
                setattr(parent, key, value)

            # Handle address updates
            if obj_in.addresses:
                existing_addresses = {pa.address_id: pa for pa in parent.addresses}

                for addr_data in obj_in.addresses:
                    address_type = addr_data.address_type
                    addr = addr_data.address

                    # Check if the same address exists
                    existing_address = (
                        self.session.query(Address)
                        .filter(
                            Address.house_no == addr.house_no,
                            Address.street_address == addr.street_address,
                            Address.landmark == addr.landmark,
                            Address.city == addr.city,
                            Address.state == addr.state,
                            Address.zip_code == addr.zip_code,
                            Address.country == addr.country
                        )
                        .first()
                    )

                    if existing_address:
                        address = existing_address
                    else:
                        address = Address(**addr.model_dump())
                        self.session.add(address)
                        self.session.flush()

                    # Update or create PersonAddress entry
                    if address.id in existing_addresses:
                        existing_pa = existing_addresses[address.id]
                        existing_pa.address_type = address_type  # Update type if needed
                    else:
                        new_pa = PersonAddress(parent_id=parent.id, address_id=address.id, address_type=address_type)
                        self.session.add(new_pa)

            self.session.commit()
            self.session.refresh(parent)
            return parent

        except IntegrityError:
            self.session.rollback()
            raise HTTPException(status_code=400, detail="Database integrity error.")
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def get_by_email(self, email: str):
        return self.session.query(Parent).filter(Parent.email == email).first()

    def get_parents_by_city(self, city: str) -> List[Parent]:
        return (
            self.session.query(Parent)
            .join(PersonAddress)
            .join(Address)
            .filter(Address.city == city)
            .all()
        )
