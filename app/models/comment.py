from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.models.base import Base, utcnow


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, default=utcnow, nullable=False)

    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    ticket = relationship("Ticket", back_populates="comments")
    author = relationship("User", back_populates="comments")
