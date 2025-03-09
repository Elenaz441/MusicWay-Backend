from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from services import VariantService
from typing import Annotated
from schemas import ShortVariantResponse, VariantResponse
from dependecies import get_current_user, get_variant_service
from exceptions import NotFoundException
from config import settings


router = APIRouter(tags=[settings.api.v1.variant.tag])


@router.get(settings.api.v1.variant.variants, response_model=list[ShortVariantResponse])
async def get_variants(
        block_id: UUID,
        payload: Annotated[dict, Depends(get_current_user)],
        variant_service: Annotated[VariantService, Depends(get_variant_service)]
):
    """Получение всех вариантов по разделу."""
    return await variant_service.get_variants_by_block(block_id)


@router.get(settings.api.v1.variant.variant, response_model=VariantResponse)
async def get_variant(
        variant_id: UUID,
        payload: Annotated[dict, Depends(get_current_user)],
        variant_service: Annotated[VariantService, Depends(get_variant_service)]
):
    try:
        return await variant_service.get_variant(variant_id, payload['role'])
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e.name))
