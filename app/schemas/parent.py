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


class PersonAddressCreate(BaseModel):
    address_type: str
    address: AddressCreate


class ParentCreate(ParentBase):
    addresses: Optional[List[PersonAddressCreate]]


class ParentUpdate(ParentBase):
    addresses: Optional[List[PersonAddressCreate]] = []


class ParentResponse(ParentBase):
    id: int
    addresses: Optional[List[PersonAddressCreate]]

    class Config:
        from_attributes = True