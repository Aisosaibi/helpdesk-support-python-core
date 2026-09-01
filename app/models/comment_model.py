from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship



if TYPE_CHECKING:
    from app.models.ticket_model import Ticket


class Comment(SQLModel, table=True):
    __tablename__ = "comments"

    id: Optional[int] = Field(default=None, primary_key=True)
    body: str = Field(max_length=5000, nullable=False)
    ticket_id: int = Field(foreign_key="tickets.id", nullable=False)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    created_at: datetime = Field(default_factory= lambda : datetime.now(timezone.utc), nullable=False)

    ticket: Optional["Ticket"] = Relationship(back_populates="comments")