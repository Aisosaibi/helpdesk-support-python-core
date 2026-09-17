from typing import Sequence

from fastapi import HTTPException, status
from app.models.ticket_model import Ticket, Status as TicketStatus, Priority as TicketPriority
from app.repositories.ticket_repository import TicketRepository
from app.repositories.user_repository import UserRepository
from app.schemas.ticket_schema import TicketCreate

ALLOWED_TRANSITIONS = {
    TicketStatus.OPEN: {TicketStatus.IN_PROGRESS},
    TicketStatus.IN_PROGRESS: {TicketStatus.CLOSED},
    TicketStatus.CLOSED: {TicketStatus.OPEN},
}


class TicketService:

    def __init__(self, repo: TicketRepository, user_repo: UserRepository):
        self.repo = repo
        self.user_repo = user_repo

    def submit_ticket(self, data: TicketCreate, user_id: int) -> Ticket:
        user = self.user_repo.get_by_id(user_id)
        if not user or not user.is_logged_in:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You must be logged in to submit a ticket",
            )
        ticket = Ticket(
            subject=data.subject,
            description=data.description,
            customer_id=data.customer_id,
            priority=data.priority,
        )
        return self.repo.create(ticket)

    def view_customer_tickets(self, customer_id: int) -> Sequence[Ticket]:
        return [ticket for ticket in self.repo.get_all() if ticket.customer_id == customer_id]

    def assign_ticket(self, ticket_id: int, agent_id: int) -> Ticket:
        ticket = self.view_ticket(ticket_id)
        agent = self.user_repo.get_by_id(agent_id)
        if not agent or agent.role.value != "agent":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
        ticket.agent_id = agent_id
        return self.repo.update(ticket)

    def view_tickets(self) -> Sequence[Ticket]:
        return self.repo.get_all()

    def ticket_summary(self) -> dict[str, int]:
        counts = {"open": 0, "in_progress": 0, "closed": 0}
        for ticket in self.repo.get_all():
            if ticket.status == TicketStatus.OPEN:
                counts["open"] += 1
            elif ticket.status == TicketStatus.IN_PROGRESS:
                counts["in_progress"] += 1
            elif ticket.status == TicketStatus.CLOSED:
                counts["closed"] += 1
        return counts

    def view_ticket(self, ticket_id: int) -> Ticket:
        ticket = self.repo.get_by_id(ticket_id)
        if not ticket:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
        return ticket

    def update_status(self, ticket_id: int, new_status: TicketStatus) -> Ticket:
        ticket = self.view_ticket(ticket_id)
        if new_status not in ALLOWED_TRANSITIONS[ticket.status]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot move ticket from {ticket.status.value} to {new_status.value}",
            )
        ticket.status = new_status
        return self.repo.update(ticket)

    def set_priority(self, ticket_id: int, new_priority: TicketPriority) -> Ticket:
        ticket = self.view_ticket(ticket_id)
        ticket.priority = new_priority
        return self.repo.update(ticket)

    def delete_ticket(self, ticket_id: int) -> None:
        ticket = self.view_ticket(ticket_id)
        self.repo.delete(ticket)
