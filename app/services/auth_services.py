from fastapi import HTTPException, status

from app.core.security import hash_password, verify_password
from app.models.user_model import User, Role
from app.repositories.user_repository import UserRepository
from app.schemas.user_schemas import UserCreate


class AuthService:

    def __init__(self, repo: UserRepository):
        self.repo = repo

    def register_user(self, data: UserCreate) -> User:
        if self.repo.get_by_email(data.email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already in use")
        user = User(name=data.name, email=data.email, password=hash_password(data.password), role=Role.customer)
        return self.repo.create(user)

    def login(self, email: str, password: str) -> User:
        user = self.repo.get_by_email(email)
        if not user or not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        user.is_logged_in = True
        return self.repo.update(user)

    def logout(self, email: str) -> None:
        user = self.repo.get_by_email(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user.is_logged_in = False
        self.repo.update(user)
