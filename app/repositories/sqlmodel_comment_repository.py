from typing import List

from sqlmodel import Session, select

from app.models.comment_model import Comment
from app.repositories.comment_repository import CommentRepository
from app.schemas.comment import CommentCreate, CommentResponse


class SqlModelCommentRepository(CommentRepository):

    def __init__(self, session: Session):
        self.session = session

    def save_comment(self, comment: CommentCreate, ticket_id: int, user_id: int) -> CommentResponse:
        new_comment = Comment(body=comment.body, ticket_id=ticket_id, user_id=user_id)
        self.session.add(new_comment)
        self.session.commit()
        self.session.refresh(new_comment)
        return CommentResponse.model_validate(new_comment)

    def get_by_ticket_id(self, ticket_id: int) -> List[CommentResponse]:
        results = self.session.exec(select(Comment).where(Comment.ticket_id == ticket_id)).all()
        return [CommentResponse.model_validate(c) for c in results]
