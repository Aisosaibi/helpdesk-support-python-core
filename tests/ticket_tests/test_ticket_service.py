import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException

from app.models.ticket_model import Ticket, Status as TicketStatus, Priority as TicketPriority
from app.models.user_model import User, Role
from app.services.ticket_service import TicketService
from app.schemas.ticket_schema import TicketCreate


@pytest.fixture
def fake_repo():
    return MagicMock()


@pytest.fixture
def fake_user_repo():
    return MagicMock()


@pytest.fixture
def service(fake_repo, fake_user_repo):
    return TicketService(fake_repo, fake_user_repo)


def test_submit_ticket_defaults_to_open(service, fake_repo, fake_user_repo):
    fake_user_repo.get_by_id.return_value = User(
        id=1, name="Ryan", email="ryan@gmail.com", password="1234", role=Role.customer, is_logged_in=True
    )
    fake_repo.create.return_value = Ticket(
        id=1, subject="No internet", description="Cannot connect", status=TicketStatus.OPEN, customer_id=1
    )
    data = TicketCreate(subject="No internet", description="Cannot connect", customer_id=1)

    result = service.submit_ticket(data, user_id=1)

    assert result.status == TicketStatus.OPEN


def test_submit_ticket_raises_401_when_not_logged_in(service, fake_repo, fake_user_repo):
    fake_user_repo.get_by_id.return_value = User(
        id=1, name="Ryan", email="ryan@gmail.com", password="1234", role=Role.customer, is_logged_in=False
    )
    data = TicketCreate(subject="No internet", description="Cannot connect", customer_id=1)

    with pytest.raises(HTTPException) as exc:
        service.submit_ticket(data, user_id=1)

    assert exc.value.status_code == 401


def test_view_ticket_raises_404_when_not_found(service, fake_repo):
    fake_repo.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc:
        service.view_ticket(99)

    assert exc.value.status_code == 404


def test_update_status_open_to_in_progress(service, fake_repo):
    ticket = Ticket(id=1, subject="Test", description="...", status=TicketStatus.OPEN, customer_id=1)
    fake_repo.get_by_id.return_value = ticket
    fake_repo.update.side_effect = lambda t: t

    result = service.update_status(1, TicketStatus.IN_PROGRESS)

    assert result.status == TicketStatus.IN_PROGRESS


def test_update_status_invalid_jump_raises_400(service, fake_repo):
    ticket = Ticket(id=1, subject="Test", description="...", status=TicketStatus.OPEN, customer_id=1)
    fake_repo.get_by_id.return_value = ticket

    with pytest.raises(HTTPException) as exc:
        service.update_status(1, TicketStatus.CLOSED)

    assert exc.value.status_code == 400


def test_set_priority_updates_ticket(service, fake_repo):
    ticket = Ticket(id=1, subject="Test", description="...", status=TicketStatus.OPEN, customer_id=1, priority=TicketPriority.LOW)
    fake_repo.get_by_id.return_value = ticket
    fake_repo.update.side_effect = lambda t: t

    result = service.set_priority(1, TicketPriority.HIGH)

    assert result.priority == TicketPriority.HIGH


def test_delete_ticket_calls_repo(service, fake_repo):
    ticket = Ticket(id=1, subject="Old", description="...", status=TicketStatus.OPEN, customer_id=1)
    fake_repo.get_by_id.return_value = ticket

    service.delete_ticket(1)

    fake_repo.delete.assert_called_once_with(ticket)
