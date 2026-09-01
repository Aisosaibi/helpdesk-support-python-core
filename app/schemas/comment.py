
from datetime import datetime
from pydantic import BaseModel, Field


class CommentCreate(BaseModel):
    body: str = Field (..., min_length=1, max_length=5000)


class CommentResponse(BaseModel):
    id: int
    body: str
    ticket_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True