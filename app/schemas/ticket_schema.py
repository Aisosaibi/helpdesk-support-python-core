from pydantic import BaseModel, ConfigDict

from app.models.ticket_model import Status


class TicketCreate(BaseModel):
    subject: str
    description: str

class TicketStatusUpdate(BaseModel):
    status: Status

class TicketOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    subject: str
    description: str
    status: str

# Do I need a dto for telling the user he deleted a ticket... what will that look like