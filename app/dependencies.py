from fastapi import Depends
from sqlmodel import Session

from app.database import get_db
from app.repositories.ticket_repository import TicketRepository
from app.repositories.sqlmodel_comment_repository import SqlModelCommentRepository
from app.services.comment_service import CommentService


def get_comment_service(session: Session = Depends(get_db)) -> CommentService:
    return CommentService(
        SqlModelCommentRepository(session),
        TicketRepository(session),
    )