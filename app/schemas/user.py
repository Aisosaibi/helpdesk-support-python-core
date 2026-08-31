import datetime
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.schemas.enum import UserRole


class UserCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=50)
    role:  UserRole = UserRole.CUSTOMER

class UserUpdate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: UserRole
    created_at: datetime
    class Config:
        from_attributes = True