import os
import pytest
from dotenv import load_dotenv
from sqlmodel import SQLModel, Session, create_engine

from app.models import Ticket, Status, User, Role
from app.repositories.ticket_repository import TicketRepository

load_dotenv()

TEST_DATABASE_URL = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}/helpdesk_test_db"
)

test_engine = create_engine(TEST_DATABASE_URL)


@pytest.fixture
def db_session():
    SQLModel.metadata.create_all(test_engine)   # build fresh tables before the test
    with Session(test_engine) as session:
        yield session                             # hand this session to the test
    SQLModel.metadata.drop_all(test_engine)      # wipe everything after the test


@pytest.fixture
def repo(db_session):
    return TicketRepository(db_session)


@pytest.fixture
def customer_id(db_session):
    # A ticket's customer_id is a real foreign key -- it has to point at
    # an actual row in `users`, not just any integer.
    user = User(name="Test Customer", email="customer@test.com", password="hashed", role=Role.customer)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user.id


def test_create_ticket_saves_and_defaults_to_open(repo, customer_id):
    ticket = Ticket(subject="Printer broken", description="Won't turn on", customer_id=customer_id)

    result = repo.create(ticket)

    assert result.id is not None
    assert result.subject == "Printer broken"
    assert result.status == Status.OPEN


def test_get_all_tickets_returns_created_ticket(repo, customer_id):
    repo.create(Ticket(subject="Wifi down", description="No connection", customer_id=customer_id))

    tickets = repo.get_all()

    assert len(tickets) == 1
    assert tickets[0].subject == "Wifi down"


def test_get_by_id_returns_none_when_missing(repo):
    result = repo.get_by_id(999)

    assert result is None


def test_delete_removes_ticket(repo, customer_id):
    ticket = repo.create(Ticket(subject="Old ticket", description="To be removed", customer_id=customer_id))

    repo.delete(ticket)

    assert repo.get_by_id(ticket.id) is None