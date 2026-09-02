from app.repositories.comment_repository import CommentRepository
from app.schemas import CommentResponse
from typing import List
from datetime import datetime, timezone

class InMemoryCommentRepository(CommentRepository):
    def __init__(self):
        self._comments: List[CommentResponse] = []
        self._next_comment_id = 1

    def save_comment(self, comment, ticket_id, user_id) -> CommentResponse:
        new_comment = CommentResponse(
            id=self._next_comment_id, body=comment.body,
            ticket_id=ticket_id, user_id=user_id,
            created_at=datetime.now(timezone.utc)
        )
        self._comments.append(new_comment)
        self._next_comment_id += 1
        return new_comment

    def get_by_ticket_id(self, ticket_id) -> List[CommentResponse]:
        return [c for c in self._comments if c.ticket_id == ticket_id]