from typing import Sequence

from fastapi import HTTPException, status
from app.models.ticket_model import Ticket, Status as TicketStatus
from app.repositories.ticket_repository import TicketRepository
from app.schemas.ticket_schema import TicketCreate

ALLOWED_TRANSITIONS = {
    TicketStatus.OPEN: {TicketStatus.IN_PROGRESS},
    TicketStatus.IN_PROGRESS: {TicketStatus.CLOSED},
    TicketStatus.CLOSED: {TicketStatus.OPEN},
}


class TicketService:
    def __init__(self, repo: TicketRepository):
        self.repo = repo

    def open_new_ticket(self, data: TicketCreate) -> Ticket:
        ticket = Ticket(subject=data.subject, description=data.description)
        return self.repo.create(ticket)

    def list_tickets(self) -> Sequence[Ticket]:
        return self.repo.get_all()

    def get_ticket(self, ticket_id: int) -> Ticket:
        ticket = self.repo.get_by_id(ticket_id)
        if not ticket:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
        return ticket

    def update_ticket_status(self, ticket_id: int, new_status: TicketStatus) -> Ticket:
        ticket = self.get_ticket(ticket_id)
        if new_status not in ALLOWED_TRANSITIONS[ticket.status]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot move ticket from {ticket.status.value} to {new_status.value}",
            )
        ticket.status = new_status
        return self.repo.update(ticket)

    def delete_ticket(self, ticket_id: int) -> None:
        ticket = self.get_ticket(ticket_id)
        self.repo.delete(ticket)