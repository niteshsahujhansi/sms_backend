from core.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, Text, Float
from sqlalchemy.orm import relationship, Mapped
from typing import List, Optional


class StudentParent(Base):
    __tablename__ = "student_parents"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    parent_id = Column(Integer, ForeignKey("parents.id", ondelete="CASCADE"), nullable=False)
    relationship_type = Column(String, nullable=False)  # E.g., "Father", "Mother", "Guardian"

    student = relationship("Student", back_populates="parent_associations")
    parent = relationship("Parent", back_populates="student_associations")


class ParentAddress(Base):
    __tablename__ = "parent_addresses"

    parent_id = Column(Integer, ForeignKey("parents.id"), primary_key=True)
    address_id = Column(Integer, ForeignKey("addresses.id"), primary_key=True)

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

    parents = relationship("Parent", secondary="parent_addresses", back_populates="addresses")

class Parent(Base):
    __tablename__ = "parents"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    # date_of_birth = Column(Date, nullable=True)
    date_of_birth = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    blood_group = Column(String, nullable=True)
    nationality = Column(String, nullable=True)
    religion = Column(String, nullable=True)
    caste_category = Column(String, nullable=False)  # Required field

    # Contact Information
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

    addresses = relationship("Address", secondary="parent_addresses", back_populates="parents")

    students = relationship("Student", secondary="student_parents", back_populates="parents", viewonly=True)
    student_associations  = relationship("StudentParent", back_populates="parent")



    

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
    caste_category = Column(String, nullable=False)  # Required field
    
    # Contact Information
    phone_number = Column(String, nullable=True)
    email = Column(String, nullable=True)
    home_address = Column(Text, nullable=True)
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
    # __table_args__ = (
    #     {'schema': 'demo'}
    # )

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)  # Secure password storage
    role = Column(String, nullable=False)  # admin, teacher, student
    is_active = Column(Boolean, default=True)




# class ParentAddress(Base):
#     __tablename__ = "parent_addresses"

#     id = Column(Integer, primary_key=True, index=True)
#     parent_id = Column(Integer, ForeignKey("parents.id", ondelete="CASCADE"), nullable=False)
#     address_id = Column(Integer, ForeignKey("addresses.id", ondelete="CASCADE"), nullable=False)
#     address_type = Column(String, nullable=False)  # E.g., "Home", "Work", "Temporary"

#     parent = relationship("Parent", back_populates="address_associations")
#     address = relationship("Address", back_populates="parent_associations")
