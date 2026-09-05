from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field


class Role(str, Enum):
    admin = "admin"
    agent = "agent"
    customer = "customer"


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    password: str
    role: Role = Role.customer
    is_logged_in: bool = Field(default=False)
