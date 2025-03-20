from fastapi import APIRouter, Depends, HTTPException, status

from services import TopicBlockService
from typing import Annotated, List
from uuid import UUID
from schemas import TopicBlockResponse, VariantStatistic
from dependecies import get_current_user, get_topic_block_service
from exceptions import NoRightsException, NotFoundException

router = APIRouter(tags=['Topic Block'])


@router.get('', response_model=List[TopicBlockResponse])
async def get_topic_blocks(
        payload: Annotated[dict, Depends(get_current_user)],
        topic_block_service: Annotated[TopicBlockService, Depends(get_topic_block_service)]
):
    """Получение всех разделов."""
    return await topic_block_service.get_blocks()


@router.get('/{block_id}/statistic', response_model=List[VariantStatistic])
async def get_topic_block_statistic(
        block_id: UUID,
        payload: Annotated[dict, Depends(get_current_user)],
        topic_block_service: Annotated[TopicBlockService, Depends(get_topic_block_service)]
):
    try:
        return await topic_block_service.get_statistic(block_id, payload['sub'], payload['role'])
    except NoRightsException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e.name))
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.name))
