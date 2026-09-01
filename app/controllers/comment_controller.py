from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from app.dependencies import get_comment_service


from app.controllers.user_controller import router
from app.schemas import CommentResponse, CommentCreate
from app.services import comment_service
from app.services.comment_service import CommentService

router = APIRouter(prefix="/ticket {ticket_id}/comment", tags=["comments"])

@router.post("/", response_model=CommentResponse,  status_code=status.HTTP_201_CREATED)
def add_cooment(
        ticket_id: int,
        comment_data: CommentCreate,
        user_id: int,
        service: CommentService = Depends(get_comment_service)

):
    try:
        return service.add_comment(ticket_id, user_id, comment_data)
    except (ValueError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=list[CommentResponse])
def get_comments(
        ticket_id: int,
        service: CommentService = Depends(get_comment_service)
):
    try:
        return service.get_comment(ticket_id)
    except (ValueError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
