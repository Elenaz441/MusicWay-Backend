from fastapi import APIRouter, Depends, HTTPException, status

from services import TopicBlockService
from typing import Annotated, List, Dict
from uuid import UUID
from schemas import TopicBlockResponse, VariantStatistic
from dependecies import get_current_user, get_topic_block_service
from exceptions import NoRightsException, NotFoundException

router = APIRouter(tags=['Topic Block'])


@router.get('', response_model=List[TopicBlockResponse])
async def get_topic_blocks(
        payload: Annotated[Dict, Depends(get_current_user)],
        topic_block_service: Annotated[TopicBlockService, Depends(get_topic_block_service)]
):
    """Получение всех разделов.

    :param payload: JWT payload текущего пользователя.
    :param topic_block_service: Сервис для работы с разделами.

    :return: Список разделов.
    """
    return await topic_block_service.get_blocks()


@router.get('/{block_id}/statistic', response_model=List[VariantStatistic])
async def get_topic_block_statistic(
        block_id: UUID,
        payload: Annotated[Dict, Depends(get_current_user)],
        topic_block_service: Annotated[TopicBlockService, Depends(get_topic_block_service)]
):
    """Возвращает статистику по разделу для ученика.

    :param block_id:
    :param payload: JWT payload текущего пользователя.
    :param topic_block_service: Сервис для работы с разделами.

    :return: Статистика по разделу.

    :raises HTTPException 403: Нет прав.
    :raises HTTPException 404: Раздел не найден.
    """
    try:
        return await topic_block_service.get_statistic(block_id, UUID(payload['sub']), payload['role'])
    except NoRightsException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e.name))
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.name))
