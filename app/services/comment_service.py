from typing import List
from urllib import response

from app.models import Status
from app.repositories.comment_repository import CommentRepository
from app.repositories.ticket_repository import TicketRepository
from app.schemas import CommentCreate, CommentResponse


class CommentService:
    def __init__(self,
                 comment_repository: CommentRepository,
                 ticket_repository: TicketRepository
                 ):
        self.lists = []
        self._comment_repository = comment_repository
        self._ticket_repository = ticket_repository


    def add_comment(self, ticket_id: int, user_id: int, data: CommentCreate) -> CommentResponse:
        responses = CommentResponse
        ticket = self._ticket_repository.get_by_id(ticket_id)
        if not ticket:
            raise ValueError("Ticket not found")
        if ticket.status == Status.CLOSED:
            raise ValueError("Ticket already closed")
        responses=  self._comment_repository.save_comment(data, ticket_id, user_id)
        return responses

    def get_comment_for_ticket(self, ticket_id: int) -> List[CommentResponse]:
        responses= CommentResponse
        ticket = self._ticket_repository.get_by_id(ticket_id)
        if not ticket:
            raise ValueError("Ticket not found")
        responses = self._comment_repository.get_by_ticket_id(ticket_id)
        self.lists.append(responses)
        return self.lists