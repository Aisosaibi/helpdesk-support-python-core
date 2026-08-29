from enum import Enum

from sqlalchemy import Column, Integer, String
from app.database import Base

class Status(Enum):
    open = "Open"
    in_progress = "In Progress"
    closed = "Closed"

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(255), nullable=False)
    description = Column(String(1000))
    status = Column(String(50), default=Status.open.value)