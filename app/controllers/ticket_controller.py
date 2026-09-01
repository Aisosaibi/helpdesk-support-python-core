from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_db
from app.repositories.ticket_repository import TicketRepository
from app.services.ticket_service import TicketService
from app.schemas.ticket_schema import TicketCreate, TicketOut, TicketStatusUpdate

router = APIRouter(prefix="/tickets", tags=["Tickets"])


def get_service(session: Session = Depends(get_db)) -> TicketService:
    return TicketService(TicketRepository(session))


@router.get("/", response_model=list[TicketOut])
def get_tickets(service: TicketService = Depends(get_service)):
    return service.list_tickets()


@router.post("/", response_model=TicketOut, status_code=201)
def create_ticket(ticket: TicketCreate, service: TicketService = Depends(get_service)):
    return service.open_new_ticket(ticket)


@router.patch("/{ticket_id}/status", response_model=TicketOut)
def update_status(ticket_id: int, payload: TicketStatusUpdate, service: TicketService = Depends(get_service)):
    return service.update_ticket_status(ticket_id, payload.status)


@router.delete("/{ticket_id}", status_code=204)
def delete_ticket(ticket_id: int, service: TicketService = Depends(get_service)):
    service.delete_ticket(ticket_id)