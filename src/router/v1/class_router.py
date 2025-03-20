from fastapi import APIRouter, Depends, HTTPException, status
from services import ClassService
from typing import Annotated, List
from uuid import UUID
from schemas import ShortClassResponse, ClassResponse, ShortLastHWTeacher, HomeworkStatistic
from dependecies import get_class_service, get_current_user
from exceptions import NoRightsException, NotFoundException


router = APIRouter(tags=['Class'])


@router.get('', response_model=List[ShortClassResponse])
async def get_classes(
        payload: Annotated[dict, Depends(get_current_user)],
        class_service: Annotated[ClassService, Depends(get_class_service)]
):
    """Получение классов преподавателя."""
    try:
        return await class_service.get_classes(UUID(payload['sub']), payload['role'])
    except NoRightsException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e.name))


@router.get('/{class_id}', response_model=ClassResponse)
async def get_class(
        class_id: UUID,
        payload: Annotated[dict, Depends(get_current_user)],
        class_service: Annotated[ClassService, Depends(get_class_service)]
):
    """Получение информации о классе"""
    try:
        return await class_service.get_class_by_id(class_id, UUID(payload['sub']), payload['role'])
    except NoRightsException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e.name))
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.name))


@router.get('/{class_id}/last_homework', response_model=List[ShortLastHWTeacher])
async def get_class_last_homework(
        class_id: UUID,
        payload: Annotated[dict, Depends(get_current_user)],
        class_service: Annotated[ClassService, Depends(get_class_service)]
):
    """Получение прошедших домашних заданий у класса"""
    try:
        return await class_service.get_last_homeworks(class_id, UUID(payload['sub']), payload['role'])
    except NoRightsException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e.name))
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.name))


@router.get('/{class_id}/statistic', response_model=List[HomeworkStatistic])
async def get_class_statistic(
        class_id: UUID,
        payload: Annotated[dict, Depends(get_current_user)],
        class_service: Annotated[ClassService, Depends(get_class_service)]
):
    """Получает статистику выполнения домашних заданий за три месяца"""
    try:
        return await class_service.get_statistic(class_id, payload['role'])
    except NoRightsException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e.name))
