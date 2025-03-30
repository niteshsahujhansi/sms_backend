from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from crud.base_crud import CRUDBase
from models.model import Parent, ParentAddress, Address
from schemas.parent import ParentCreate, ParentUpdate
from typing import List

class ParentCRUD(CRUDBase[Parent, ParentCreate]):
    def __init__(self, db: Session):
        super().__init__(Parent, db)  # Pass db to the base class

    def create(self, obj_in: ParentCreate):
        try:
            # Extract addresses from input
            address_data = obj_in.addresses  # List of address objects
            
            new_addresses = []
            linked_addresses = []
            parent_address_associations = []  # To store ParentAddress objects

            if address_data:
                for addr_data in address_data:
                    address_type = addr_data.address_type
                    addr = addr_data.address  # Extract address fields
                    
                    # Check if the same address exists
                    existing_address = (
                        self.db.query(Address)
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
                        self.db.add(address)
                        new_addresses.append(address)

                    self.db.flush()  # Ensure new addresses get an ID
                    
                    # Create ParentAddress entry
                    parent_address = ParentAddress(
                        address_id=address.id,  # ✅ Corrected: Use address_id, not address
                        address_type=address_type
                    )
                    parent_address_associations.append(parent_address)

            # Create Parent (excluding addresses)
            parent = Parent(**obj_in.model_dump(exclude={"addresses"}))

            # Commit parent first to get the ID
            self.db.add(parent)
            self.db.flush()

            # Link addresses to the parent
            for pa in parent_address_associations:
                pa.parent_id = parent.id  # Assign parent ID after creation
                self.db.add(pa)

            self.db.commit()
            self.db.refresh(parent)
            return parent

        # except IntegrityError:
        #     self.db.rollback()
        #     raise HTTPException(status_code=400, detail="Database integrity error.")
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def update(self, parent_id: int, obj_in: ParentUpdate):
        try:
            parent = self.db.query(Parent).filter(Parent.id == parent_id).first()
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
                        self.db.query(Address)
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
                        self.db.add(address)
                        self.db.flush()

                    # Update or create ParentAddress entry
                    if address.id in existing_addresses:
                        existing_pa = existing_addresses[address.id]
                        existing_pa.address_type = address_type  # Update type if needed
                    else:
                        new_pa = ParentAddress(parent_id=parent.id, address_id=address.id, address_type=address_type)
                        self.db.add(new_pa)

            self.db.commit()
            self.db.refresh(parent)
            return parent

        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Database integrity error.")
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))


    def create_without_manytomany(self, obj_in: ParentCreate):
        # Extract addresses from input
        address_data = obj_in.addresses  # List of addresses

        new_addresses = []
        linked_addresses = []
        if address_data is not None:
            for addr in address_data:
                # Check if an identical address exists in the database
                existing_address = (
                    self.db.query(Address)
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
                    linked_addresses.append(existing_address)  # Use existing address
                else:
                    new_address = Address(**addr.model_dump())
                    self.db.add(new_address)
                    new_addresses.append(new_address)

        # Flush new addresses to get their IDs before linking them
        self.db.flush()

        # Create Parent with linked addresses
        parent = Parent(
            **obj_in.model_dump(exclude={"addresses"})  # Unpack all fields except addresses
        )
        parent.addresses = linked_addresses + new_addresses  # Link existing & new addresses

        self.db.add(parent)
        self.db.commit()
        self.db.refresh(parent)
        return parent

    def update_old(self, parent_id: int, obj_in: ParentUpdate):
        db_parent = self.db.query(Parent).filter(Parent.id == parent_id).first()
        if not db_parent:
            raise HTTPException(status_code=404, detail="Parent not found")

        # Update Parent fields
        for key, value in obj_in.model_dump(exclude={"address"}).items():
            setattr(db_parent, key, value)

        # Process address updates (if provided)
        if obj_in.address:
            self.db.query(ParentAddress).filter(ParentAddress.parent_id == parent_id).delete()

            for addr in obj_in.address:
                existing_address = (
                    self.db.query(Address)
                    .filter(
                        Address.street == addr.street,
                        Address.city == addr.city,
                        Address.state == addr.state,
                        Address.postal_code == addr.postal_code,
                        Address.country == addr.country,
                    )
                    .first()
                )

                if not existing_address:
                    existing_address = Address(
                        street=addr.street,
                        city=addr.city,
                        state=addr.state,
                        postal_code=addr.postal_code,
                        country=addr.country,
                    )
                    self.db.add(existing_address)
                    self.db.flush()

                parent_address = ParentAddress(
                    parent_id=parent_id,
                    address_id=existing_address.id,
                    address_type=addr.address_type,
                )
                self.db.add(parent_address)

        self.db.commit()
        self.db.refresh(db_parent)
        return db_parent

    def get_by_email(self, email: str):
        return self.db.query(Parent).filter(Parent.email == email).first()

    def get_parents_by_city(self, city: str) -> List[Parent]:
        return (
            self.db.query(Parent)
            .join(ParentAddress)
            .join(Address)
            .filter(Address.city == city)
            .all()
        )




    def createe(self, obj_in: ParentCreate):
        # Extract address details from the payload
        address_data = obj_in.address  # List of address with types

        # Create Parent (excluding address)
        parent_data = obj_in.model_dump(exclude={"address"})
        parent = Parent(**parent_data)
        self.db.add(parent)
        self.db.flush()  # Flush to get parent.id before adding relationships

        # Process address
        for addr in address_data:
            # Check if the address already exists
            existing_address = (
                self.db.query(Address)
                .filter(
                    Address.street == addr.street,
                    Address.city == addr.city,
                    Address.state == addr.state,
                    Address.postal_code == addr.postal_code,
                    Address.country == addr.country,
                )
                .first()
            )

            if not existing_address:
                # Create a new address if it does not exist
                existing_address = Address(
                    street=addr.street,
                    city=addr.city,
                    state=addr.state,
                    postal_code=addr.postal_code,
                    country=addr.country,
                )
                self.db.add(existing_address)
                self.db.flush()  # Get address.id

            # Create Parent-Address association
            parent_address = ParentAddress(
                parent_id=parent.id,
                address_id=existing_address.id,
                address_type=addr.address_type,
            )
            self.db.add(parent_address)

        try:
            self.db.commit()
            self.db.refresh(parent)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Integrity error while creating parent.")
        
        return parent


    def create_using_address_id(self, obj_in: ParentCreate):
        # Extract addresses from input
        address_data = obj_in.addresses  # List of addresses

        existing_addresses={}
        new_addresses = []
        
        if address_data is not None:
        
            # Check if addresses already exist
            existing_addresses = {addr.id: addr for addr in self.db.query(Address).filter(Address.id.in_([a.id for a in address_data])).all()}

            # Create new addresses if they don't exist
            new_addresses = []
            for addr in address_data:
                if addr.id not in existing_addresses:
                    new_address = Address(**addr.model_dump())
                    self.db.add(new_address)
                    new_addresses.append(new_address)
            
            # Flush new addresses to get their IDs before linking them
            self.db.flush()

        # # Create Parent with linked addresses
        # parent = Parent(
        #     name=obj_in.name,
        #     email=obj_in.email,
        #     phone=obj_in.phone,
        #     occupation=obj_in.occupation,
        #     # address_type="a",
        #     addresses=list(existing_addresses.values()) + new_addresses
        # )

        # Create Parent with linked addresses (optimized)
        parent = Parent(
            **obj_in.model_dump(exclude={"addresses"})  # Unpacks all fields except addresses
        )
        parent.addresses = list(existing_addresses.values()) + new_addresses

        self.db.add(parent)
        self.db.commit()
        self.db.refresh(parent)
        return parent
