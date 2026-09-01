import os
import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine

from app.main import app
from app.database import get_db
from app.models import User, Role

load_dotenv()

TEST_DATABASE_URL = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}/helpdesk_test_db"
)

test_engine = create_engine(TEST_DATABASE_URL)


def override_get_db():
    with Session(test_engine) as session:
        yield session


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_and_teardown():
    SQLModel.metadata.create_all(test_engine)
    yield
    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture
def customer_id():
    # The controller tests go through the real HTTP layer, so we seed the
    # user directly in the test DB first -- same reasoning as the repository
    # tests: customer_id is a real foreign key, not an arbitrary integer.
    with Session(test_engine) as session:
        user = User(name="Test Customer", email="customer@test.com", password="hashed", role=Role.customer)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user.id


def test_create_and_list_tickets(customer_id):
    response = client.post(
        "/tickets/",
        json={"subject": "Broken chair", "description": "Leg is loose", "customer_id": customer_id},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["subject"] == "Broken chair"
    assert data["status"] == "open"

    response = client.get("/tickets/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_update_ticket_status_for_valid_transition(customer_id):
    create_response = client.post(
        "/tickets/",
        json={"subject": "Slow laptop", "description": "Takes forever", "customer_id": customer_id},
    )
    ticket_id = create_response.json()["id"]

    response = client.patch(f"/tickets/{ticket_id}/status", json={"status": "in-progress"})
    assert response.status_code == 200
    assert response.json()["status"] == "in-progress"

    # in-progress -> open is not a legal transition
    response = client.patch(f"/tickets/{ticket_id}/status", json={"status": "open"})
    assert response.status_code == 400


def test_update_ticket_status_rejects_invalid_jump(customer_id):
    create_response = client.post(
        "/tickets/",
        json={"subject": "New printer", "description": "Needs setup", "customer_id": customer_id},
    )
    ticket_id = create_response.json()["id"]

    # open -> closed is not a legal transition
    response = client.patch(f"/tickets/{ticket_id}/status", json={"status": "closed"})
    assert response.status_code == 400


def test_delete_ticket_returns_204(customer_id):
    create_response = client.post(
        "/tickets/",
        json={"subject": "Temp", "description": "...", "customer_id": customer_id},
    )
    ticket_id = create_response.json()["id"]

    response = client.delete(f"/tickets/{ticket_id}")
    assert response.status_code == 204