from typing import Optional, Sequence
from sqlmodel import Session, select
from app.models.ticket_model import Ticket


class TicketRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, ticket: Ticket) -> Ticket:
        self.session.add(ticket)
        self.session.commit()
        self.session.refresh(ticket)
        return ticket

    def get_all(self) -> Sequence[Ticket]:
        return self.session.exec(select(Ticket)).all()

    def get_by_id(self, ticket_id: int) -> Optional[Ticket]:
        return self.session.get(Ticket, ticket_id)

    def update(self, ticket: Ticket) -> Ticket:
        self.session.add(ticket)
        self.session.commit()
        self.session.refresh(ticket)
        return ticket

    def delete(self, ticket: Ticket) -> None:
        self.session.delete(ticket)
        self.session.commit()