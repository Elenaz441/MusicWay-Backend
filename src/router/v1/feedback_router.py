from fastapi import APIRouter, Depends, HTTPException, status
from services import FeedbackService
from typing import Annotated, Dict
from schemas import CreateFeedback
from dependecies import get_feedback_service, get_current_user
from exceptions import NoRightsException, NotFoundException


router = APIRouter(tags=['Feedback'])


@router.post('', status_code=status.HTTP_201_CREATED)
async def submit_feedback(
        feedback: CreateFeedback,
        payload: Annotated[Dict, Depends(get_current_user)],
        feedback_server: Annotated[FeedbackService, Depends(get_feedback_service)]
):
    """Отправка обратной связи.

    :param feedback: Данные об обратной связи.
    :param payload: JWT payload текущего пользователя.
    :param feedback_server: Сервис работы с обратной связью.

    :return: Сообщение об успешной отправке.

    :raises HTTPException 403: Нет прав на отправку.
    :raises HTTPException 404: Материал не найден."""
    try:
        await feedback_server.create_feedback(feedback, payload['role'])
        return {'message': 'Обратная связь отправлена.'}
    except NoRightsException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e.name))
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.name))
