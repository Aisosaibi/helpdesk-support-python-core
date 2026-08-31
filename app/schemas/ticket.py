from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.enum import TicketStatus
from app.schemas.enum import TicketStatus, TicketPriority



class TicketCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=50)
    description: str = Field(..., min_length=2, max_length=100)
    priority: TicketPriority = TicketPriority.MEDIUM

class TicketUpdateStatus(BaseModel):
    status: TicketStatus

class TicketUpdatePriority(BaseModel):
    priority: TicketPriority

class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    status: TicketStatus
    priority: TicketPriority
    user_id: int
    created_at: datetime
    updated_at: datetime
    assigned_to_id: Optional[int] = None
    class Config:
        from_attributes = True



