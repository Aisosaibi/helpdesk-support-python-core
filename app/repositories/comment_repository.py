from typing import List

from sqlmodel import Session, select

from app.models.comment_model import Comment
from app.schemas.comment import CommentCreate, CommentResponse


class CommentRepository:
    """Persist comments through the same SQLModel database as other repositories."""

    def __init__(self, session: Session):
        self.session = session

    def save_comment(self, comment: CommentCreate, ticket_id: int, user_id: int) -> CommentResponse:
        new_comment = Comment(
            body=comment.body,
            ticket_id=ticket_id,
            user_id=user_id,
        )
        self.session.add(new_comment)
        self.session.commit()
        self.session.refresh(new_comment)
        return CommentResponse.model_validate(new_comment)

    def get_by_ticket_id(self, ticket_id: int) -> List[CommentResponse]:
        statement = select(Comment).where(Comment.ticket_id == ticket_id)
        comments = self.session.exec(statement).all()
        return [CommentResponse.model_validate(comment) for comment in comments]
