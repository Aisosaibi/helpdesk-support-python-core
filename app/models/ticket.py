import enum

from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.models.base import Base, utcnow


class TicketStatus(enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketPriority(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(Enum(TicketStatus), default=TicketStatus.OPEN, nullable=False)
    priority = Column(Enum(TicketPriority), default=TicketPriority.MEDIUM, nullable=False)
    created_at = Column(DateTime, default=utcnow, nullable=False)

    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    agent_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    customer = relationship(
        "User",
        foreign_keys=[customer_id],
        back_populates="tickets_created",
    )

    agent = relationship(
        "User",
        foreign_keys=[agent_id],
        back_populates="tickets_assigned",
    )

    category = relationship("Category", back_populates="tickets")

    comments = relationship(
        "Comment",
        back_populates="ticket",
        cascade="all, delete-orphan",
    )

    def assign_to_agent(self, agent):
        self.agent = agent

    def update_status(self, new_status):
        self.status = new_status
