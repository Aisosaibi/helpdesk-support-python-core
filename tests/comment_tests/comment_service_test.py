# tests/test_comment_service.py
from datetime import datetime, timezone
from typing import Optional

import pytest

from app.models.ticket_model import Status, Priority, Ticket
from app.repositories.in_memory_comment_repository import InMemoryCommentRepository
from app.schemas import CommentCreate
from app.services.comment_service import CommentService


class FakeTicketRepository:

    def __init__(self):
        self._tickets: dict[int, Ticket] = {}

    def add_ticket(self, ticket: Ticket):
        self._tickets[ticket.id] = ticket

    def get_by_id(self, ticket_id: int) -> Optional[Ticket]:
        return self._tickets.get(ticket_id)


def make_ticket(id: int, status: Status) -> Ticket:
    return Ticket(
        id=id,
        subject="Sample ticket",
        description="Sample description",
        status=status,
        priority=Priority.LOW,
        customer_id=1,
        created_at=datetime.now(timezone.utc),
    )


@pytest.fixture
def service():
    comment_repo = InMemoryCommentRepository()
    ticket_repo = FakeTicketRepository()
    ticket_repo.add_ticket(make_ticket(id=1, status=Status.OPEN))
    ticket_repo.add_ticket(make_ticket(id=2, status=Status.CLOSED))
    return CommentService(comment_repo, ticket_repo)


def test_add_comment_returns_comment_with_correct_body(service):
    comment = service.add_comment(ticket_id=1, user_id=42, data=CommentCreate(body="Greetings from the great guy"))

    assert comment.body == "Greetings from the great guy"
    assert comment.ticket_id == 1
    assert comment.user_id == 42


def test_add_comment_raises_when_ticket_does_not_exist(service):
    with pytest.raises(ValueError, match="Ticket not found"):
        service.add_comment(ticket_id=999, user_id=42, data=CommentCreate(body="Wagwan"))


def test_add_comment_raises_when_ticket_is_closed(service):
    with pytest.raises(ValueError, match="Ticket already closed"):
        service.add_comment(ticket_id=2, user_id=42, data=CommentCreate(body="What's Good nigga"))


def test_get_comments_for_ticket_returns_only_that_tickets_comments(service):
    service.add_comment(ticket_id=1, user_id=1, data=CommentCreate(body="First comment"))
    service.add_comment(ticket_id=1, user_id=2, data=CommentCreate(body="Second comment"))

    comments = service.get_comments_for_ticket(1)

    assert len(comments) == 2
    assert comments[0].body == "First comment"
    assert comments[1].body == "Second comment"


def test_get_comments_for_ticket_raises_when_ticket_does_not_exist(service):
    with pytest.raises(ValueError, match="Ticket not found"):
        service.get_comments_for_ticket(999)