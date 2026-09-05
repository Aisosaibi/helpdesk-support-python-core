from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_db
from app.repositories.user_repository import UserRepository
from app.services.auth_services import AuthService
from app.schemas.user_schemas import LoginRequest, LoginResponse, LogoutRequest, UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_service(session: Session = Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(session))


@router.post("/register", response_model=UserResponse, status_code=201)
def register(data: UserCreate, service: AuthService = Depends(get_service)):
    user = service.register_user(data)
    return UserResponse.model_validate(user)


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, service: AuthService = Depends(get_service)):
    user = service.login(data.email, data.password)
    return LoginResponse(message="Login successful", user=UserResponse.model_validate(user))


@router.post("/logout", status_code=200)
def logout(data: LogoutRequest, service: AuthService = Depends(get_service)):
    service.logout(data.email)
    return {"message": "Logged out successfully"}
