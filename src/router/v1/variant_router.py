from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from services import VariantService
from typing import Annotated, Dict, List
from schemas import ShortVariantResponse, VariantResponse
from dependecies import get_current_user, get_variant_service
from exceptions import NotFoundException


router = APIRouter(tags=['Variant'])


@router.get('', response_model=List[ShortVariantResponse])
async def get_variants(
        block_id: UUID,
        payload: Annotated[Dict, Depends(get_current_user)],
        variant_service: Annotated[VariantService, Depends(get_variant_service)]
):
    """Получение всех вариантов по разделу.

    :param block_id: Идентификатор раздела.
    :param payload: JWT payload текущего пользователя.
    :param variant_service: Сервис для работы с вариантами.

    :return: Список вариантов по разделу
    """
    return await variant_service.get_variants_by_block(block_id, payload['role'])


@router.get('/{variant_id}', response_model=VariantResponse)
async def get_variant(
        variant_id: UUID,
        payload: Annotated[Dict, Depends(get_current_user)],
        variant_service: Annotated[VariantService, Depends(get_variant_service)]
):
    """Получение информации о варианте.

    :param variant_id: Идентификатор варианта.
    :param payload: JWT payload текущего пользователя.
    :param variant_service: Сервис для работы с вариантами.

    :return: Информация о варианте упражнения.
    """
    try:
        return await variant_service.get_variant(variant_id, payload['role'])
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.name))
