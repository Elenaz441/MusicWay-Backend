from fastapi import APIRouter, Depends

from services import TopicBlockService
from typing import Annotated, List
from schemas import TopicBlockResponse
from dependecies import get_current_user, get_topic_block_service

router = APIRouter(tags=['Topic Block'])


@router.get('', response_model=List[TopicBlockResponse])
async def get_topic_blocks(
        payload: Annotated[dict, Depends(get_current_user)],
        topic_block_service: Annotated[TopicBlockService, Depends(get_topic_block_service)]
):
    """Получение всех разделов."""
    return await topic_block_service.get_blocks()
