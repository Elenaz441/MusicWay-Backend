from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from services import MaterialService
from typing import Annotated, List, Dict
from schemas import ShortMaterialResponse, MaterialVideoResponse, MaterialTextResponse, VariantForActiveTask
from dependecies import get_current_user, get_material_service
from exceptions import NotFoundException


router = APIRouter(tags=['Study material'])


@router.get('', response_model=List[ShortMaterialResponse])
async def get_materials(
        block_id: UUID,
        payload: Annotated[Dict, Depends(get_current_user)],
        material_service: Annotated[MaterialService, Depends(get_material_service)]
):
    """Получение всех материалов по разделу.

    :param block_id: Идентификатор раздела (блока).
    :param payload: JWT payload текущего пользователя.
    :param material_service: Сервис для работы с материалами.

    :return: Список материалов."""
    return await material_service.get_materials_by_block(block_id)


@router.get('/{material_id}/video', response_model=MaterialVideoResponse)
async def get_material_video(
        material_id: UUID,
        payload: Annotated[Dict, Depends(get_current_user)],
        material_service: Annotated[MaterialService, Depends(get_material_service)]
):
    """Получение видео материала по его идентификатору.

    :param material_id: Идентификатор материала.
    :param payload: JWT payload текущего пользователя.
    :param material_service: Сервис для работы с материалами.

    :return: Видео-материал.

    :raises HTTPException 404: Материал не найден."""
    try:
        return await material_service.get_video(material_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.name))


@router.get('/{material_id}/text', response_model=MaterialTextResponse)
async def get_material_text(
        material_id: UUID,
        payload: Annotated[Dict, Depends(get_current_user)],
        material_service: Annotated[MaterialService, Depends(get_material_service)]
):
    """Получение текста материала по его идентификатору.

    :param material_id: Идентификатор материала.
    :param payload: JWT payload текущего пользователя.
    :param material_service: Сервис для работы с материалами.

    :return: Текст материала.

    :raises HTTPException 404: Материал не найден."""
    try:
        return await material_service.get_text(material_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.name))


@router.get('/{material_id}/tasks', response_model=List[VariantForActiveTask])
async def get_material_tasks(
        material_id: UUID,
        payload: Annotated[Dict, Depends(get_current_user)],
        material_service: Annotated[MaterialService, Depends(get_material_service)]
):
    """Получение списка упражнений, связанных с учебным материалом.

    :param material_id: Идентификатор учебного материала.
    :param payload: JWT payload текущего пользователя.
    :param material_service: Сервис для работы с материалами.

    :return: Список упражнений.

    :raises HTTPException 404: Материал не найден.
    """
    try:
        return await material_service.get_tasks(material_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.name))


@router.get('/search', response_model=List[ShortMaterialResponse])
async def get_materials(
        query: str,
        payload: Annotated[Dict, Depends(get_current_user)],
        material_service: Annotated[MaterialService, Depends(get_material_service)]
):
    """Поиск учебных материалов по ключевому слову.

    :param query: Поисковый запрос.
    :param payload: JWT payload текущего пользователя.
    :param material_service: Сервис для работы с материалами.

    :return: Список материалов, соответствующих запросу."""
    return await material_service.search_materials(query)
