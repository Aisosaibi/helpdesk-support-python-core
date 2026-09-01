from typing import Optional
from pydantic import BaseModel
from app.models.user_model import Role


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: Role = Role.customer


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[Role] = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: Role

    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    message: str
    user: UserResponse
