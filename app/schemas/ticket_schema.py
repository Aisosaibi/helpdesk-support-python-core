from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.ticket_model import Status, Priority


class TicketCreate(BaseModel):
    subject: str
    description: str
    customer_id: int
    priority: Priority = Priority.LOW


class TicketStatusUpdate(BaseModel):
    status: Status


class TicketPriorityUpdate(BaseModel):
    priority: Priority


class TicketOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    subject: str
    description: str
    status: str
    priority: str
    customer_id: int
    agent_id: int | None = None
    created_at: datetime | None = None


class TicketSummary(BaseModel):
    open: int
    in_progress: int
    closed: int
