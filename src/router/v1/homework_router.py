from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from services import HomeworkService
from typing import Annotated, List, Union
from schemas import ShortActiveHomework, ShortLastHomework, ActiveHomework, LastHomework, TeacherHomework, CreateHomework, EditHomework
from dependecies import get_current_user, get_homework_service
from config import settings
from exceptions import NotFoundException, NoRightsException, IncorrectDataException


router = APIRouter(tags=[settings.api.v1.homework.tag])


@router.post('/create', response_model=UUID)
async def create_homework(
        homework_data: CreateHomework,
        payload: Annotated[dict, Depends(get_current_user)],
        homework_service: Annotated[HomeworkService, Depends(get_homework_service)]
):
    """Создание домашнего задания."""
    try:
        hw_id = await homework_service.create_homework(homework_data, payload['role'])
        return hw_id
    except NoRightsException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e.name))


@router.get('', response_model=List[Union[ShortActiveHomework, ShortLastHomework]])
async def get_homework(
        active: bool,
        payload: Annotated[dict, Depends(get_current_user)],
        homework_service: Annotated[HomeworkService, Depends(get_homework_service)]
):
    """Получение списка домашних заданий."""
    try:
        return await homework_service.get_homeworks_by_user(UUID(payload['sub']), active)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.name))


@router.get('/{homework_id}/active', response_model=ActiveHomework)
async def get_active_homework(
        homework_id: UUID,
        payload: Annotated[dict, Depends(get_current_user)],
        homework_service: Annotated[HomeworkService, Depends(get_homework_service)]
):
    """Получение активного домашнего задания"""
    try:
        return await homework_service.get_active_homework(homework_id, payload['sub'], payload['role'])
    except NoRightsException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e.name))
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.name))
    except IncorrectDataException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.name))


@router.get('/{homework_id}/completed', response_model=LastHomework)
async def get_completed_homework(
        homework_id: UUID,
        payload: Annotated[dict, Depends(get_current_user)],
        homework_service: Annotated[HomeworkService, Depends(get_homework_service)]
):
    """Получение завершенного домашнего задания"""
    try:
        return await homework_service.get_completed_homework(homework_id, payload['sub'], payload['role'])
    except NoRightsException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e.name))
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.name))
    except IncorrectDataException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.name))


@router.get('/{homework_id}', response_model=TeacherHomework)
async def get_homework(
        homework_id: UUID,
        payload: Annotated[dict, Depends(get_current_user)],
        homework_service: Annotated[HomeworkService, Depends(get_homework_service)]
):
    """Получение домашнего задания для учителя."""
    try:
        return await homework_service.get_homework(homework_id, payload['role'])
    except NoRightsException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e.name))
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.name))


@router.patch('/{homework_id}', response_model=UUID)
async def update_homework(
        homework_id: UUID,
        homework_data: EditHomework,
        payload: Annotated[dict, Depends(get_current_user)],
        homework_service: Annotated[HomeworkService, Depends(get_homework_service)]
):
    """Обновление домашнего задания"""
    try:
        return await homework_service.edit_homework(homework_id, homework_data, payload['role'])
    except NoRightsException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e.name))


@router.delete('/{homework_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_homework(
        homework_id: UUID,
        payload: Annotated[dict, Depends(get_current_user)],
        homework_service: Annotated[HomeworkService, Depends(get_homework_service)]
):
    """Удаление домашнего задания"""
    try:
        return await homework_service.delete_homework(homework_id, payload['role'])
    except NoRightsException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e.name))

