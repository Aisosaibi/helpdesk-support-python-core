from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_db
from app.repositories.ticket_repository import TicketRepository
from app.repositories.user_repository import UserRepository
from app.services.ticket_service import TicketService
from app.schemas.ticket_schema import (
    TicketCreate,
    TicketOut,
    TicketPriorityUpdate,
    TicketStatusUpdate,
    TicketSummary,
)

router = APIRouter(prefix="/tickets", tags=["Tickets"])


def get_service(session: Session = Depends(get_db)) -> TicketService:
    return TicketService(TicketRepository(session), UserRepository(session))


@router.get("/", response_model=list[TicketOut])
def get_tickets(service: TicketService = Depends(get_service)):
    return service.view_tickets()


@router.get("/summary", response_model=TicketSummary)
def get_ticket_summary(service: TicketService = Depends(get_service)):
    return service.ticket_summary()


@router.get("/customer/{customer_id}", response_model=list[TicketOut])
def get_customer_tickets(customer_id: int, service: TicketService = Depends(get_service)):
    return service.view_customer_tickets(customer_id)


@router.get("/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: int, service: TicketService = Depends(get_service)):
    return service.view_ticket(ticket_id)


@router.post("/", response_model=TicketOut, status_code=201)
def create_ticket(ticket: TicketCreate, user_id: int, service: TicketService = Depends(get_service)):
    return service.submit_ticket(ticket, user_id)


@router.patch("/{ticket_id}/status", response_model=TicketOut)
def update_ticket_status(ticket_id: int, payload: TicketStatusUpdate, service: TicketService = Depends(get_service)):
    return service.update_status(ticket_id, payload.status)


@router.patch("/{ticket_id}/assign", response_model=TicketOut)
def assign_ticket(ticket_id: int, agent_id: int, service: TicketService = Depends(get_service)):
    return service.assign_ticket(ticket_id, agent_id)


@router.patch("/{ticket_id}/priority", response_model=TicketOut)
def update_ticket_priority(ticket_id: int, payload: TicketPriorityUpdate, service: TicketService = Depends(get_service)):
    return service.set_priority(ticket_id, payload.priority)


@router.delete("/{ticket_id}", status_code=204)
def delete_ticket(ticket_id: int, service: TicketService = Depends(get_service)):
    service.delete_ticket(ticket_id)
