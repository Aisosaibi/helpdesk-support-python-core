from typing import List

from app.models.ticket_model import Status
from app.repositories.comment_repository import CommentRepository
from app.repositories.ticket_repository import TicketRepository
from app.schemas.comment import CommentCreate, CommentResponse


class CommentService:

    def __init__(self, comment_repository: CommentRepository, ticket_repository: TicketRepository):
        self._comment_repository = comment_repository
        self._ticket_repository = ticket_repository

    def add_comment(self, ticket_id: int, user_id: int, data: CommentCreate) -> CommentResponse:
        ticket = self._ticket_repository.get_by_id(ticket_id)
        if not ticket:
            raise ValueError("Ticket not found")
        if ticket.status == Status.CLOSED:
            raise ValueError("Ticket already closed")
        return self._comment_repository.save_comment(data, ticket_id, user_id)

    def get_comments_for_ticket(self, ticket_id: int) -> List[CommentResponse]:
        ticket = self._ticket_repository.get_by_id(ticket_id)
        if not ticket:
            raise ValueError("Ticket not found")
        return self._comment_repository.get_by_ticket_id(ticket_id)
