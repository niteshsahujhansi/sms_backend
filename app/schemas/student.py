from pydantic import BaseModel, EmailStr, Field 
from typing import List, Optional, Union
from uuid import UUID

from datetime import date, datetime

from schemas.parent import ParentResponse
from schemas.common_schemas import CamelCaseModel,  AddressBase

from utils.constants import FileCategoryEnum, FileTypeEnum, RelatedEntityEnum, UserRoleEnum, VirusScanStatusEnum, FileStatusEnum


class MedicalDetailBase(CamelCaseModel):
    medical_conditions: Optional[str] = None
    allergies: Optional[str] = None
    doctor_name: Optional[str] = None
    doctor_contact: Optional[str] = None
    health_insurance_details: Optional[str] = None

class MedicalDetailResponse(MedicalDetailBase):
    id: int

class TransportDetailBase(CamelCaseModel):
    hostel_required: Optional[bool] = False
    hostel_room_number: Optional[str] = None
    day_scholar: Optional[bool] = True
    transport_required: Optional[bool] = False
    pickup_location: Optional[str] = None
    bus_route_number: Optional[str] = None

class TransportDetailResponse(TransportDetailBase):
    id: int


class StudentBase(CamelCaseModel):
    first_name: str
    caste_category: str
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    nationality: Optional[str] = None
    religion: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    # home_address: Optional[str] = None

    # Contact Information
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relationship: Optional[str] = None

    # Academic Information
    student_id: Optional[str] = None
    roll_number: Optional[str] = None
    grade: Optional[str] = None
    section: Optional[str] = None
    previous_school_name: Optional[str] = None
    enrollment_date: Optional[date] = None
    medium_of_instruction: Optional[str] = None
    house: Optional[str] = None

    # Documents & Identification
    aadhaar_number: Optional[str] = None
    birth_certificate: Optional[str] = None
    previous_school_tc: Optional[str] = None
    caste_certificate: Optional[str] = None
    student_photo: Optional[str] = None
    parent_photo: Optional[str] = None

class ParentData(CamelCaseModel):
    id: int
    relationship: str

class AddressData(CamelCaseModel):
    address_type: str  # "Current" or "Permanent"
    address: AddressBase

class StudentCreate(StudentBase):
    # relationship: str  # Ensure this is required
    # parent_ids: List[int] = []  # List of existing parent IDs
    parent_data: Optional[List[ParentData]] = None  # Update to accept relationships
    address_data: Optional[List[AddressData]] = None
    # address_data: Optional[List[AddressData]] = []

class StudentUpdate(StudentBase):
    parent_data: Optional[List[ParentData]] = None

class StudentParentAssociationResponse(BaseModel):
    # relationship_type: str
    relationship_type: str
    parent: ParentResponse


class StudentResponse(StudentBase):
    id: int
    parent_associations: List[StudentParentAssociationResponse]
    # parent_data: Optional[List[ParentData]] = None
    medical_details: Optional[MedicalDetailResponse] = None
    transport_details: Optional[TransportDetailResponse] = None
    
    class Config:
        from_attributes = True
        alias_generator = lambda s: ''.join([s.split('_')[0]] + [w.capitalize() for w in s.split('_')[1:]])
        populate_by_name = True









# class StudentBase(BaseModel):
#     name: str = Field(..., min_length=2, max_length=50, description="Student's full name")
#     email: EmailStr  # Already validated by Pydantic
#     age: int = Field(..., ge=3, le=100, description="Student's age must be between 3 and 100")
#     grade: int = Field(..., ge=0, le=12, description="Student's grade (must be between 1 and 12)")
#     section: str = Field(..., pattern="^[A-D]$", description="Section must be A, B, C, or D")

    # class Config:
    #     orm_mode = True


# class StudentCreate(StudentBase):
#     pass



# class StudentResponse(StudentBase):
#     id: UUID

#     class Config:
#         from_attributes = True  # Allows conversion from ORM models