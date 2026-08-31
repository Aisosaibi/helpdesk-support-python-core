from fastapi import HTTPException, status

from app.core.security import hash_password
from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schemas import UserCreate, UserUpdate


class UserService:

    def __init__(self, repo: UserRepository):
        self.repo = repo

    def get_all_users(self) -> list[User]:
        return self.repo.get_all()

    def get_user(self, user_id: int) -> User:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    def create_user(self, data: UserCreate) -> User:
        if self.repo.get_by_email(data.email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already in use")
        user = User(name=data.name, email=data.email, password=hash_password(data.password), role=data.role)
        return self.repo.create(user)

    def update_user(self, user_id: int, data: UserUpdate) -> User:
        user = self.get_user(user_id)
        if data.name is not None:
            user.name = data.name
        if data.email is not None:
            user.email = data.email
        if data.password is not None:
            user.password = hash_password(data.password)
        if data.role is not None:
            user.role = data.role
        return self.repo.update(user)

    def delete_user(self, user_id: int) -> None:
        user = self.get_user(user_id)
        self.repo.delete(user)
