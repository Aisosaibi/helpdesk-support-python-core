from abc import abstractmethod, ABC
from typing import List

from app.schemas import CommentCreate, CommentResponse

class CommentRepository(ABC):

    @abstractmethod
    def save_comment(self, comment: CommentCreate, ticket_id: int, user_id: int ) -> CommentResponse:
        pass

    @abstractmethod
    def get_by_ticket_id(self, ticket_id: int) -> List[CommentResponse]:
        pass