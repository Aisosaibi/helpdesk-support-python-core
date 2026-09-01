import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException

from app.models.ticket_model import Ticket, Status
from app.services.ticket_service import TicketService
from app.schemas.ticket_schema import TicketCreate


@pytest.fixture
def fake_repo():
    # A blank stand-in for TicketRepository. It has no behavior yet --
    # each test below tells it what to say when asked.
    return MagicMock()


@pytest.fixture
def service(fake_repo):
    return TicketService(fake_repo)


def test_open_new_ticket_defaults_to_open_status(service, fake_repo):
    fake_repo.create.return_value = Ticket(
        id=1, subject="Wifi down", description="Cannot connect", status=TicketStatus.OPEN
    )
    ticket_data = TicketCreate(subject="Wifi down", description="Cannot connect")

    result = service.open_new_ticket(ticket_data)

    assert result.status == TicketStatus.OPEN
    fake_repo.create.assert_called_once()


def test_get_ticket_raises_404_when_missing(service, fake_repo):
    fake_repo.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        service.get_ticket(999)

    assert exc_info.value.status_code == 404


def test_update_ticket_status_allows_valid_transition(service, fake_repo):
    ticket = Ticket(id=1, subject="Slow laptop", description="...", status=TicketStatus.OPEN)
    fake_repo.get_by_id.return_value = ticket
    fake_repo.update.side_effect = lambda t: t  # echo back the mutated ticket

    result = service.update_ticket_status(1, TicketStatus.IN_PROGRESS)

    assert result.status == TicketStatus.IN_PROGRESS
    fake_repo.update.assert_called_once()


def test_update_ticket_status_rejects_invalid_jump(service, fake_repo):
    ticket = Ticket(id=1, subject="Slow laptop", description="...", status=TicketStatus.OPEN)
    fake_repo.get_by_id.return_value = ticket

    with pytest.raises(HTTPException) as exc_info:
        service.update_ticket_status(1, TicketStatus.CLOSED)

    assert exc_info.value.status_code == 400
    fake_repo.update.assert_not_called()


def test_delete_ticket_calls_repo_delete(service, fake_repo):
    ticket = Ticket(id=1, subject="Old", description="...", status=TicketStatus.OPEN)
    fake_repo.get_by_id.return_value = ticket

    service.delete_ticket(1)

    fake_repo.delete.assert_called_once_with(ticket)


def test_close_all_tickets_closes_only_in_progress(service, fake_repo):
    open_ticket = Ticket(id=1, subject="a", description="a", status=TicketStatus.OPEN)
    in_progress = Ticket(id=2, subject="b", description="b", status=TicketStatus.IN_PROGRESS)
    already_closed = Ticket(id=3, subject="c", description="c", status=TicketStatus.CLOSED)
    fake_repo.get_all.return_value = [open_ticket, in_progress, already_closed]
    fake_repo.update.side_effect = lambda t: t

    result = service.close_all_tickets()

    assert len(result) == 1
    assert result[0] is in_progress
    assert in_progress.status == TicketStatus.CLOSED
    fake_repo.update.assert_called_once()