from pydantic import BaseModel, EmailStr
from typing import Optional


# ✅ Schema for user creation (input)
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str  # Plain text password (will be hashed before saving)
    role: str  # Example: "admin", "teacher", "student"


# ✅ Schema for returning user data (response)
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        from_attributes = True  # Allows ORM model conversion


# ✅ Schema for authentication (login request)
class UserLogin(BaseModel):
    username: str
    password: str


# ✅ Schema for updating a user (optional fields)
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
