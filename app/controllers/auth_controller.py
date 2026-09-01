from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_db
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.schemas.user_schemas import LoginRequest, LoginResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_service(session: Session = Depends(get_db)) -> UserService:
    return UserService(UserRepository(session))


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, service: UserService = Depends(get_service)):
    """Send your email and password. If they match, you get back your user info."""
    user = service.login_user(data.email, data.password)
    return LoginResponse(
        message="Login successful",
        user=UserResponse.model_validate(user),
    )

@router.post("/logout", status_code=200)
def logout():
    """Logout endpoint. Just returns a goodbye message."""
    return {"message": "Logged out successfully"}
