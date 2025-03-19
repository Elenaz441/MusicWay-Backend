from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from services import MaterialService
from typing import Annotated, List
from schemas import ShortMaterialResponse, MaterialVideoResponse, MaterialTextResponse, VariantForActiveTask
from dependecies import get_current_user, get_material_service
from exceptions import NotFoundException


router = APIRouter(tags=['Study material'])


@router.get('', response_model=List[ShortMaterialResponse])
async def get_materials(
        block_id: UUID,
        payload: Annotated[dict, Depends(get_current_user)],
        material_service: Annotated[MaterialService, Depends(get_material_service)]
):
    """Получение всех материалов по разделу."""
    return await material_service.get_materials_by_block(block_id)


@router.get('/{material_id}/video', response_model=MaterialVideoResponse)
async def get_material_video(
        material_id: UUID,
        payload: Annotated[dict, Depends(get_current_user)],
        material_service: Annotated[MaterialService, Depends(get_material_service)]
):
    try:
        return await material_service.get_video(material_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.name))


@router.get('/{material_id}/text', response_model=MaterialTextResponse)
async def get_material_text(
        material_id: UUID,
        payload: Annotated[dict, Depends(get_current_user)],
        material_service: Annotated[MaterialService, Depends(get_material_service)]
):
    try:
        return await material_service.get_text(material_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.name))


@router.get('/{material_id}/tasks', response_model=List[VariantForActiveTask])
async def get_material_tasks(
        material_id: UUID,
        payload: Annotated[dict, Depends(get_current_user)],
        material_service: Annotated[MaterialService, Depends(get_material_service)]
):
    try:
        return await material_service.get_tasks(material_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.name))


@router.get('/search', response_model=List[ShortMaterialResponse])
async def get_materials(
        query: str,
        payload: Annotated[dict, Depends(get_current_user)],
        material_service: Annotated[MaterialService, Depends(get_material_service)]
):
    """Получение всех разделов."""
    return await material_service.search_materials(query)
