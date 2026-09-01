
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class Comment(SQLModel, table=True):
    __tablename__ = "comments"

    id: Optional[int] = Field(default=None, primary_key=True)
    body: str = Field(max_length=5000, nullable=False)
    ticket_id: int = Field(foreign_key="ticket.id", nullable=False)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    created_at: datetime = Field(default_factory= lambda : datetime.utcnow(), nullable=False)