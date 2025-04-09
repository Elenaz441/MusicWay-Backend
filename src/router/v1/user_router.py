from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from services import UserService
from typing import Annotated, Dict
from schemas import UserStatistic
from dependecies import get_current_user, get_user_service
from exceptions import NoRightsException, NotFoundException

router = APIRouter(tags=['User'])


@router.get('/statistic', response_model=UserStatistic)
async def get_statistic(
        payload: Annotated[Dict, Depends(get_current_user)],
        user_service: Annotated[UserService, Depends(get_user_service)]
):
    """Получение статистики ученика.

    :param payload: JWT payload текущего пользователя.
    :param user_service: Сервис для работы с пользователями.

    :return: Процент успешности.

    :raises HTTPException 403: Нет прав.
    :raises HTTPException 404: Класс не найден.
    """
    try:
        return await user_service.get_statistic(UUID(payload['sub']), payload['role'])
    except NoRightsException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e.name))
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.name))
