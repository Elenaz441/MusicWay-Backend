from fastapi import APIRouter, Depends, HTTPException, status
from services import FeedbackService
from typing import Annotated
from schemas import CreateFeedback
from config import settings
from dependecies import get_feedback_service, get_current_user
from exceptions import NoRightsException, NotFoundException


router = APIRouter(tags=[settings.api.v1.feedback.tag])


@router.post(settings.api.v1.feedback.create_feedback, status_code=status.HTTP_201_CREATED)
async def submit_feedback(
        feedback: CreateFeedback,
        payload: Annotated[dict, Depends(get_current_user)],
        feedback_server: Annotated[FeedbackService, Depends(get_feedback_service)]
):
    """Регистрация нового пользователя."""
    try:
        await feedback_server.create_feedback(feedback, payload['role'])
        return {'message': 'Обратная связь отправлена.'}
    except NoRightsException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e.name))
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.name))
