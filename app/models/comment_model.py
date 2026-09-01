from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

from app.models.ticket_model import Ticket


class Comment(SQLModel, table=True):
    __tablename__ = "comments"

    id: Optional[int] = Field(default=None, primary_key=True)
    message: str
    ticket_id: int = Field(foreign_key="tickets.id")
    user_id: int = Field(foreign_key="users.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    is_deleted: bool = Field(default=False)

    ticket: Optional["Ticket"] = Relationship(back_populates="comments")