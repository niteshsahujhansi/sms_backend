from core.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB

from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Boolean, Text, JSON, Enum, BigInteger, text, Float

from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional
from sqlalchemy.sql import func
from utils.constants import RelatedEntityEnum, FileCategoryEnum, FileTypeEnum, UserRoleEnum, FileStatusEnum, VirusScanStatusEnum


# Enum for Gender / Blood Group / Caste:
# remove nulable true 
# Use RS256 (RSA keypair):

class StudentParent(Base):
    __tablename__ = "student_parents"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    parent_id = Column(Integer, ForeignKey("parents.id", ondelete="CASCADE"), nullable=False)
    relationship_type = Column(String, nullable=False)  # E.g., "Father", "Mother", "Guardian"

    student = relationship("Student", back_populates="parent_associations", lazy='selectin')
    parent = relationship("Parent", back_populates="student_associations", lazy='selectin')


class PersonAddress(Base):
    __tablename__ = "parent_addresses"

    id = Column(Integer, primary_key=True, index=True , autoincrement=True)
    parent_id = Column(Integer, ForeignKey("parents.id"), nullable=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=True)
    teacher_id = Column(UUID(as_uuid=True), ForeignKey("teachers.id"), nullable=True)
    address_id = Column(Integer, ForeignKey("addresses.id"), nullable=False)
    address_type = Column(String, nullable=False)

    address = relationship("Address", back_populates="persons", lazy='selectin')
    parent = relationship("Parent", back_populates="addresses", lazy='selectin')
    student = relationship("Student", back_populates="addresses", lazy='selectin')
    teacher = relationship("Teacher", back_populates="addresses", lazy='selectin')


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

    persons = relationship("PersonAddress", back_populates="address", lazy='selectin')


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
    email = Column(String, unique=True)
    emergency_contact_name = Column(String, nullable=True)
    emergency_contact_phone = Column(String, nullable=True)
    emergency_contact_relationship = Column(String, nullable=True)

    occupation = Column(String, nullable=True)
    designation = Column(String, nullable=True)
    company_name = Column(String, nullable=True)
    # annual_income = Column(String, nullable=True)

    aadhaar_number = Column(String, nullable=True)
    passport_number = Column(String, nullable=True)
    driving_license_number = Column(String, nullable=True)
    PAN_number = Column(String, nullable=True)
    annual_income = Column(String, nullable=True)

    photo = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    preferred_language = Column(String, nullable=True)
    communication_preference = Column(String, nullable=True)

    students = relationship("Student", secondary="student_parents", back_populates="parents", viewonly=True, lazy='selectin')
    student_associations  = relationship("StudentParent", back_populates="parent", lazy='selectin')

    addresses = relationship("PersonAddress", back_populates="parent", cascade="all, delete-orphan", lazy='selectin')


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
    email = Column(String, unique=True)
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
    medical_details = relationship("MedicalDetail", back_populates="student", uselist=False, lazy='selectin')
    transport_details = relationship("TransportDetail", back_populates="student", uselist=False, lazy='selectin')

    # Relationship with parents via association table
    parent_associations = relationship("StudentParent", back_populates="student", cascade="all, delete-orphan", lazy='selectin')
    parents = relationship("Parent", secondary="student_parents", back_populates="students", viewonly=True, lazy='selectin')

    addresses = relationship("PersonAddress", back_populates="student", cascade="all, delete-orphan", lazy='selectin')

    # --- Classes and Subjects ---

    class_associations = relationship("ClassStudent", back_populates="student", cascade="all, delete-orphan", lazy='selectin')
    classes = relationship("Class", secondary="class_students", back_populates="students", viewonly=True, lazy='selectin')


class MedicalDetail(Base):
    __tablename__ = "medical_details"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    medical_conditions = Column(Text, nullable=True)
    allergies = Column(Text, nullable=True)
    doctor_name = Column(String, nullable=True)
    doctor_contact = Column(String, nullable=True)
    health_insurance_details = Column(String, nullable=True)

    student = relationship("Student", back_populates="medical_details", lazy='selectin')


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

    student = relationship("Student", back_populates="transport_details", lazy='selectin')


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


class Tenant_db_Master(Base):
    __tablename__ = "tenant_db_master"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4(), index=True, nullable=False)
    tenant_id = mapped_column(Integer, nullable=False)
    db_user = mapped_column(String, unique=True, nullable=False)
    db_password = mapped_column(String, unique=True, nullable=False)
    db_host = mapped_column(String, unique=True, nullable=False)
    db_port = mapped_column(String, unique=True, nullable=False)
    db_name = mapped_column(String, unique=True, nullable=False)


class UserMaster(Base):
    __tablename__ = "user_master"
    
    id = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4(), index=True, nullable=False)
    tenant_id = mapped_column(Integer, nullable=False)
    username = mapped_column(String, unique=True, index=True, nullable=False)
    email = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password = mapped_column(String, nullable=False)
    role = mapped_column(String, nullable=False)
    salt = mapped_column(String(256), nullable=False)
    force_password = mapped_column(Boolean, server_default=text('true'), nullable=False)
    is_mfa = mapped_column(Boolean, server_default=text('true'), nullable=False)
    is_sso = mapped_column(Boolean, server_default=text('false'), nullable=False)
    otp = mapped_column(String(10))
    otp_expiry = mapped_column(DateTime)
    failed_login_attempts = mapped_column(Integer, server_default=text('0'), nullable=False)
    is_account_lock = mapped_column(Boolean, server_default=text('false'), nullable=False)
    locked_until = mapped_column(DateTime)
    last_login_at = mapped_column(DateTime)
    last_password_changed_at = mapped_column(DateTime)
    last_passwords = mapped_column(ARRAY(String), nullable=True)
    is_active = mapped_column(Boolean, server_default=text('true'), nullable=False)
    is_deleted = mapped_column(Boolean, server_default=text('false'), nullable=False)
    created_at = mapped_column(DateTime, server_default=func.now(), nullable=False)
    created_by = mapped_column(String(512))
    updated_at = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    updated_by = mapped_column(String(512))


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4(), index=True, nullable=False)
    
    # Personal Information
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String, nullable=True)
    blood_group = Column(String, nullable=True)
    nationality = Column(String, nullable=True)
    religion = Column(String, nullable=True)
    
    # Contact Information
    phone = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    emergency_contact_name = Column(String, nullable=True)
    emergency_contact_phone = Column(String, nullable=True)
    emergency_contact_relationship = Column(String, nullable=True)
    
    # Professional Information
    employee_id = Column(String, nullable=False)
    # employee_id = Column(String, unique=True, nullable=False)
    joining_date = Column(Date, nullable=False)
    qualifications = Column(ARRAY(String), nullable=False)
    specializations = Column(ARRAY(String), nullable=True)
    experience_years = Column(Integer, nullable=True)
    previous_schools = Column(String, nullable=True)
    designation = Column(String, nullable=True)
    department = Column(String, nullable=True)
    teaching_subjects = Column(ARRAY(String), nullable=True)
    preferred_grades = Column(ARRAY(String), nullable=True)
    
    # Documents
    photo = Column(String, nullable=True)
    resume = Column(String, nullable=True)
    qualification_certificates = Column(ARRAY(String), nullable=True)
    experience_certificates = Column(ARRAY(String), nullable=True)
    id_proof = Column(String, nullable=True)
    address_proof = Column(String, nullable=True)
    aadhaar_number = Column(String, nullable=True)
    pan_number = Column(String, nullable=True)
    
    # Additional Information
    preferred_language = Column(String, nullable=True)
    communication_preference = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    addresses = relationship("PersonAddress", back_populates="teacher", cascade="all, delete-orphan", lazy='selectin')
    class_teacher_for = relationship("Class", back_populates="class_teacher", lazy='selectin')
    subject_associations = relationship("SubjectTeacher", back_populates="teacher", cascade="all, delete-orphan", lazy='selectin')
    subjects = relationship("Subject", secondary="subject_teachers", back_populates="teachers", viewonly=True, lazy='selectin')

    # def __repr__(self):
    #     return f"<Teacher {self.first_name} {self.last_name}>"

# --- Classes and Subjects (with extended columns) ---

class Class(Base):
    __tablename__ = "classes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # e.g., "Class 1"
    section = Column(String, nullable=True)  # e.g., "A"
    academic_year = Column(String, nullable=True)  # e.g., "2024-2025"
    class_teacher_id = Column(UUID(as_uuid=True), ForeignKey("teachers.id"), nullable=True)
    room_number = Column(String, nullable=True)
    max_students = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(String, nullable=True)
    updated_by = Column(String, nullable=True)

    class_teacher = relationship("Teacher", back_populates="class_teacher_for", lazy='selectin')
    student_associations = relationship("ClassStudent", back_populates="klass", cascade="all, delete-orphan", lazy='selectin')
    students = relationship("Student", secondary="class_students", back_populates="classes", viewonly=True, lazy='selectin')
    subject_associations = relationship("ClassSubject", back_populates="klass", cascade="all, delete-orphan", lazy='selectin')
    subjects = relationship("Subject", secondary="class_subjects", back_populates="classes", viewonly=True, lazy='selectin')

class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # e.g., "Mathematics"
    code = Column(String, nullable=True)   # e.g., "MATH101"
    description = Column(Text, nullable=True)
    syllabus = Column(Text, nullable=True)
    credits = Column(Integer, nullable=True)
    is_elective = Column(Boolean, default=False)
    subject_type = Column(String, nullable=True)  # core/elective/lab/practical
    max_marks = Column(Integer, nullable=True)
    department = Column(String, nullable=True)
    language = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(String, nullable=True)
    updated_by = Column(String, nullable=True)

    class_associations = relationship("ClassSubject", back_populates="subject", cascade="all, delete-orphan", lazy='selectin')
    classes = relationship("Class", secondary="class_subjects", back_populates="subjects", viewonly=True, lazy='selectin')
    teacher_associations = relationship("SubjectTeacher", back_populates="subject", cascade="all, delete-orphan", lazy='selectin')
    teachers = relationship("Teacher", secondary="subject_teachers", back_populates="subjects", viewonly=True, lazy='selectin')

class ClassStudent(Base):
    __tablename__ = "class_students"
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    enrollment_date = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(String, nullable=True)
    updated_by = Column(String, nullable=True)

    student = relationship("Student", back_populates="class_associations", lazy='selectin')
    klass = relationship("Class", back_populates="student_associations", lazy='selectin')

class ClassSubject(Base):
    __tablename__ = "class_subjects"
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    assigned_date = Column(Date, nullable=True)
    is_optional = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(String, nullable=True)
    updated_by = Column(String, nullable=True)

    klass = relationship("Class", back_populates="subject_associations", lazy='selectin')
    subject = relationship("Subject", back_populates="class_associations", lazy='selectin')

class SubjectTeacher(Base):
    __tablename__ = "subject_teachers"
    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    teacher_id = Column(UUID(as_uuid=True), ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False)
    assigned_date = Column(Date, nullable=True)
    is_primary = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(String, nullable=True)
    updated_by = Column(String, nullable=True)

    subject = relationship("Subject", back_populates="teacher_associations", lazy='selectin')
    teacher = relationship("Teacher", back_populates="subject_associations", lazy='selectin')