from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, EmailStr, Field, UUID4
from .common_schemas import CamelCaseModel, AddressBase, AddressCreate

class TeacherAddressCreate(CamelCaseModel):
    address_type: str
    address: AddressCreate

class TeacherBase(CamelCaseModel):
    # Personal Information
    first_name: str
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    nationality: Optional[str] = None
    religion: Optional[str] = None
    
    # Contact Information
    phone: Optional[str] = None
    email: EmailStr
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relationship: Optional[str] = None
    
    # Professional Information
    employee_id: str
    joining_date: date
    qualifications: List[str]
    specializations: Optional[List[str]] = None
    experience_years: Optional[int] = None
    previous_schools: Optional[str] = None
    designation: Optional[str] = None
    department: Optional[str] = None
    teaching_subjects: Optional[List[str]] = None
    preferred_grades: Optional[List[str]] = None
    
    # Documents
    photo: Optional[str] = None
    resume: Optional[str] = None
    qualification_certificates: Optional[List[str]] = None
    experience_certificates: Optional[List[str]] = None
    id_proof: Optional[str] = None
    address_proof: Optional[str] = None
    aadhaar_number: Optional[str] = None
    pan_number: Optional[str] = None
    
    # Additional Information
    preferred_language: Optional[str] = None
    communication_preference: Optional[str] = None
    notes: Optional[str] = None

    # Addresses
    addresses: Optional[List[TeacherAddressCreate]] = None

class TeacherCreate(TeacherBase):
    pass

class TeacherUpdate(TeacherBase):
    pass

class TeacherResponse(TeacherBase):
    id: UUID4
    is_active: bool
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TeacherResponseMessage(BaseModel):
    id: UUID4
    message: str 