from fastapi import Depends
from sqlmodel import Session

from app.database import get_db
from app.repositories.ticket_repository import TicketRepository
from app.repositories.comment_repository import CommentRepository
from app.services.comment_service import CommentService


def get_comment_service(session: Session = Depends(get_db)) -> CommentService:
    return CommentService(
        CommentRepository(session),
        TicketRepository(session),
    )
