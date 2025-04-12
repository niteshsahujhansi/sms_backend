from core.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB

from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Boolean, Text, JSON, Enum, BigInteger

from sqlalchemy.orm import relationship, Mapped
from typing import List, Optional
from sqlalchemy.sql import func
from utils.constants import RelatedEntityEnum, FileCategoryEnum, FileTypeEnum, UserRoleEnum, FileStatusEnum, VirusScanStatusEnum




class StudentParent(Base):
    __tablename__ = "student_parents"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    parent_id = Column(Integer, ForeignKey("parents.id", ondelete="CASCADE"), nullable=False)
    relationship_type = Column(String, nullable=False)  # E.g., "Father", "Mother", "Guardian"

    student = relationship("Student", back_populates="parent_associations")
    parent = relationship("Parent", back_populates="student_associations")


class PersonAddress(Base):
    __tablename__ = "parent_addresses"

    id = Column(Integer, primary_key=True, index=True , autoincrement=True)
    parent_id = Column(Integer, ForeignKey("parents.id"), nullable=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=True)
    address_id = Column(Integer, ForeignKey("addresses.id"), primary_key=True)
    address_type = Column(String, nullable=False)

    address = relationship("Address", back_populates="persons")
    parent = relationship("Parent", back_populates="addresses")
    student = relationship("Student", back_populates="addresses")


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    house_no = Column(String, nullable=False)
    street_address = Column(String, nullable=False)
    landmark = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    country = Column(String, nullable=False)

    persons = relationship("PersonAddress", back_populates="address")


class Parent(Base):
    __tablename__ = "parents"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    date_of_birth = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    blood_group = Column(String, nullable=True)
    nationality = Column(String, nullable=True)
    religion = Column(String, nullable=True)
    caste_category = Column(String, nullable=True)

    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    emergency_contact_name = Column(String, nullable=True)
    emergency_contact_phone = Column(String, nullable=True)
    emergency_contact_relationship = Column(String, nullable=True)

    occupation = Column(String, nullable=True)
    designation = Column(String, nullable=True)
    company_name = Column(String, nullable=True)
    annual_income = Column(String, nullable=True)

    aadhaar_number = Column(String, nullable=True)
    passport_number = Column(String, nullable=True)
    driving_license_number = Column(String, nullable=True)
    PAN_number = Column(String, nullable=True)
    annual_income = Column(String, nullable=True)

    photo = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    preferred_language = Column(String, nullable=True)
    communication_preference = Column(String, nullable=True)

    students = relationship("Student", secondary="student_parents", back_populates="parents", viewonly=True)
    student_associations  = relationship("StudentParent", back_populates="parent")

    addresses = relationship("PersonAddress", back_populates="parent", cascade="all, delete-orphan")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    
    # Personal Information
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String, nullable=True)
    blood_group = Column(String, nullable=True)
    nationality = Column(String, nullable=True)
    religion = Column(String, nullable=True)
    caste_category = Column(String, nullable=False)
    
    # Contact Information
    phone_number = Column(String, nullable=True)
    email = Column(String, nullable=True)
    # home_address = Column(Text, nullable=True)
    emergency_contact_name = Column(String, nullable=True)
    emergency_contact_phone = Column(String, nullable=True)
    emergency_contact_relationship = Column(String, nullable=True)

    # Academic Information
    student_id = Column(String, nullable=True)
    roll_number = Column(String, nullable=True)
    grade = Column(String, nullable=True)
    section = Column(String, nullable=True)
    previous_school_name = Column(String, nullable=True)
    enrollment_date = Column(Date, nullable=True)
    medium_of_instruction = Column(String, nullable=True)
    house = Column(String, nullable=True)

    # Documents & Identification
    aadhaar_number = Column(String, nullable=True)
    birth_certificate = Column(String, nullable=True)  # Will store file path
    previous_school_tc = Column(String, nullable=True)  # Will store file path
    caste_certificate = Column(String, nullable=True)  # Will store file path
    student_photo = Column(String, nullable=True)  # Will store file path
    parent_photo = Column(String, nullable=True)  # Will store file path
    
    # Relationships
    medical_details = relationship("MedicalDetail", back_populates="student", uselist=False)
    transport_details = relationship("TransportDetail", back_populates="student", uselist=False)

    # Relationship with parents via association table
    parent_associations = relationship("StudentParent", back_populates="student", cascade="all, delete-orphan")
    parents = relationship("Parent", secondary="student_parents", back_populates="students", viewonly=True)

    addresses = relationship("PersonAddress", back_populates="student", cascade="all, delete-orphan")


class MedicalDetail(Base):
    __tablename__ = "medical_details"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    medical_conditions = Column(Text, nullable=True)
    allergies = Column(Text, nullable=True)
    doctor_name = Column(String, nullable=True)
    doctor_contact = Column(String, nullable=True)
    health_insurance_details = Column(String, nullable=True)

    student = relationship("Student", back_populates="medical_details")


class TransportDetail(Base):
    __tablename__ = "transport_details"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    hostel_required = Column(Boolean, nullable=True, default=False)
    hostel_room_number = Column(String, nullable=True)
    day_scholar = Column(Boolean, nullable=True, default=True)
    transport_required = Column(Boolean, nullable=True, default=False)
    pickup_location = Column(String, nullable=True)
    bus_route_number = Column(String, nullable=True)

    student = relationship("Student", back_populates="transport_details")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)  # Secure password storage
    role = Column(String, nullable=False)  # admin, teacher, student
    is_active = Column(Boolean, default=True)


class Upload(Base):
    __tablename__ = "upload"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False, index=True)
    
    original_filename = Column(String) # when download give actuall filename
    file_extension = Column(String) # 1-Fast Filtering & Searching, 2-UI/UX Use Cases, 3-/images/, /docs/, 4-Cleaner Reporting
    content_type = Column(String)
    file_size = Column(BigInteger) # 1-Show file size in the UI, 2-Validate or Filter on File Size, Quota Tracking / Limit Enforcing (SUM(file_size) for a user)
    checksum = Column(String)  # SHA256/MD5 (optional)
    storage_path = Column(String, nullable=False)
    file_category = Column(Enum(FileCategoryEnum), default=FileCategoryEnum.miscellaneous)
    file_type = Column(Enum(FileTypeEnum), nullable=False, default=FileTypeEnum.other)
    url = Column(Text, nullable=True)
    expiry_at = Column(DateTime, nullable=True)
    
    is_private = Column(Boolean, default=True)
    status = Column(Enum(FileStatusEnum), default=FileStatusEnum.archived)
    virus_scan_status = Column(Enum(VirusScanStatusEnum), default=VirusScanStatusEnum.pending)
    
    related_entity = Column(Enum(RelatedEntityEnum), default=RelatedEntityEnum.unknown)
    related_entity_id = Column(Integer, nullable=True, index=True)
    related_entity_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.unknown)

    is_active = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)

    uploaded_by_id = Column(UUID(as_uuid=True))
    uploaded_by_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.unknown)
    uploaded_at = Column(DateTime, server_default=func.now())
    
    updated_by_id = Column(UUID(as_uuid=True))
    updated_by_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.unknown)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # tags = Column(ARRAY(String))
    # metadata = Column(JSONB)

    # app.mount("/static", StaticFiles(directory="uploads"), name="static")
