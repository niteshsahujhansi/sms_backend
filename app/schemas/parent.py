from pydantic import BaseModel, EmailStr, Field 
from uuid import UUID

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date

from schemas.common_schemas import CamelCaseModel, AddressCreate, AddressResponse

class ParentBase(CamelCaseModel):

    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    nationality: Optional[str] = None
    religion: Optional[str] = None
    caste_category: Optional[str] = None

    phone: Optional[str] = None
    email: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relationship: Optional[str] = None

    occupation: Optional[str] = None
    designation: Optional[str] = None
    company_name: Optional[str] = None
    annual_income: Optional[str] = None

    aadhaar_number: Optional[str] = None
    passport_number: Optional[str] = None
    driving_license_number: Optional[str] = None
    PAN_number: Optional[str] = None
    annual_income: Optional[str] = None

    photo: Optional[str] = None
    notes: Optional[str] = None
    preferred_language: Optional[str] = None
    communication_preference: Optional[str] = None

class ParentCreate(ParentBase):
    addresses: list[AddressCreate] = None  # Nested Address object

class ParentUpdate(ParentBase):
    address: list[AddressCreate] = None  # Optional for updating

class ParentResponse(ParentBase):
    id: int
    # address: list[AddressResponse] = None  # Include Address in response

    class Config:
        from_attributes = True  # ORM mode for SQLAlchemy

    # class Config:
    #     orm_mode = True  # Enables ORM to Pydantic conversion
    #     alias_generator = lambda x: ''.join([x[0].lower()] + [y.capitalize() for y in x.split('_')[1:]])  
    #     populate_by_name = True  # Allows using both snake_case & camelCase

    # class Config:
    #     alias_generator = lambda x: ''.join([x[0].lower()] + [y.capitalize() for y in x.split('_')[1:]])
    #     populate_by_name = True
    
    # class Config:
    #     alias_generator = lambda x: ''.join([x[0].lower(), x.title()[1:]])  # Auto-convert to camelCase
    #     allow_population_by_field_name = True



    # class Config:
    #     alias_generator = lambda s: ''.join([s.split('_')[0]] + [w.capitalize() for w in s.split('_')[1:]])  # Converts to camelCase
    #     populate_by_name = True

    # class Config:
    #     alias_generator = lambda s: ''.join([s.split('_')[0]] + [w.capitalize() for w in s.split('_')[1:]])
    #     populate_by_name = True