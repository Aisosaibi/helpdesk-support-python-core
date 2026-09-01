from datetime import datetime
from abc import ABC
from typing import List
from app.repositories.comment_repository import CommentRepository
from app.schemas import CommentResponse, CommentCreate


class InMemoryCommentRepository(CommentRepository):
    def __init__(self):
        self._comments: List[CommentResponse] = []
        self._next_comment_id = 1

    def save_comment(self, comment: CommentCreate, ticket_id:int, user_id: int) -> CommentResponse:
        new_comment = CommentResponse(
            id=self._next_comment_id,
            body=comment.body,
            ticket_id=ticket_id,
            user_id=user_id,
            created_at=datetime.now(datetime.timezone.utc)
        )
        self._comments.append(new_comment)
        self._next_comment_id += 1
        return new_comment

    def get_by_ticket_id(self, ticket_id:int) -> List[CommentResponse]:
        return [comment for comment in self._comments if comment.ticket_id == ticket_id]
