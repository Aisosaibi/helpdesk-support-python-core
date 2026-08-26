import enum

from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from app.models.base import Base


class Role(enum.Enum):
    CUSTOMER = "customer"
    AGENT = "agent"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(Role), default=Role.CUSTOMER, nullable=False)

    tickets_created = relationship(
        "Ticket",
        foreign_keys="Ticket.customer_id",
        back_populates="customer",
    )

    tickets_assigned = relationship(
        "Ticket",
        foreign_keys="Ticket.agent_id",
        back_populates="agent",
    )

    comments = relationship(
        "Comment",
        back_populates="author",
    )
