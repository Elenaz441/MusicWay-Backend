from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from services import MaterialService
from typing import Annotated
from schemas import ShortMaterialResponse, MaterialVideoResponse, MaterialTextResponse
from dependecies import get_current_user, get_material_service
from exceptions import NotFoundException
from config import settings


router = APIRouter(tags=[settings.api.v1.material.tag])


@router.get(settings.api.v1.material.materials, response_model=list[ShortMaterialResponse])
async def get_materials(
        block_id: UUID,
        payload: Annotated[dict, Depends(get_current_user)],
        material_service: Annotated[MaterialService, Depends(get_material_service)]
):
    """Получение всех разделов."""
    return await material_service.get_materials(block_id)


@router.get(settings.api.v1.material.video, response_model=MaterialVideoResponse)
async def get_material_video(
        material_id: UUID,
        payload: Annotated[dict, Depends(get_current_user)],
        material_service: Annotated[MaterialService, Depends(get_material_service)]
):
    try:
        return await material_service.get_video(material_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e.name))


@router.get(settings.api.v1.material.text, response_model=MaterialTextResponse)
async def get_material_text(
        material_id: UUID,
        payload: Annotated[dict, Depends(get_current_user)],
        material_service: Annotated[MaterialService, Depends(get_material_service)]
):
    try:
        return await material_service.get_text(material_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e.name))


@router.get(settings.api.v1.material.search, response_model=list[ShortMaterialResponse])
async def get_materials(
        query: str,
        payload: Annotated[dict, Depends(get_current_user)],
        material_service: Annotated[MaterialService, Depends(get_material_service)]
):
    """Получение всех разделов."""
    return await material_service.search_materials(query)
