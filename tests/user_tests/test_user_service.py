import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException

from app.models.user_model import User, Role
from app.services.user_service import UserService
from app.schemas.user_schemas import UserCreate, UserUpdate


@pytest.fixture
def fake_repo():
    return MagicMock()


@pytest.fixture
def service(fake_repo):
    return UserService(fake_repo)


def test_register_user_succeeds(service, fake_repo):
    fake_repo.get_by_email.return_value = None
    fake_repo.create.return_value = User(id=1, name="Ali", email="ali@test.com", password="hashed", role=Role.customer)

    result = service.register_user(UserCreate(name="Ali", email="ali@test.com", password="1234", role=Role.customer))

    assert result.email == "ali@test.com"
    fake_repo.create.assert_called_once()


def test_register_user_raises_409_on_duplicate_email(service, fake_repo):
    fake_repo.get_by_email.return_value = User(id=1, name="Ali", email="ali@test.com", password="hashed", role=Role.customer)

    with pytest.raises(HTTPException) as exc:
        service.register_user(UserCreate(name="Ali", email="ali@test.com", password="1234", role=Role.customer))

    assert exc.value.status_code == 409


def test_get_user_by_id_raises_404_when_not_found(service, fake_repo):
    fake_repo.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc:
        service.get_user_by_id(99)

    assert exc.value.status_code == 404


def test_delete_user_calls_repo(service, fake_repo):
    user = User(id=1, name="Ali", email="ali@test.com", password="hashed", role=Role.customer)
    fake_repo.get_by_id.return_value = user

    service.delete_user(1)

    fake_repo.delete.assert_called_once_with(user)


def test_login_raises_401_on_wrong_password(service, fake_repo):
    fake_repo.get_by_email.return_value = None

    with pytest.raises(HTTPException) as exc:
        service.login("ali@test.com", "wrongpassword")

    assert exc.value.status_code == 401
