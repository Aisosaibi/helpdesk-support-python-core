from fastapi import APIRouter, HTTPException, Depends, status

from app.dependencies import get_comment_service
from app.schemas.comment import CommentCreate, CommentResponse
from app.services.comment_service import CommentService

router = APIRouter(prefix="/tickets/{ticket_id}/comments", tags=["Comments"])


@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def add_comment(
    ticket_id: int,
    comment_data: CommentCreate,
    user_id: int,
    service: CommentService = Depends(get_comment_service),
):
    try:
        return service.add_comment(ticket_id, user_id, comment_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=list[CommentResponse])
def get_comments(
    ticket_id: int,
    service: CommentService = Depends(get_comment_service),
):
    try:
        return service.get_comments_for_ticket(ticket_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
