from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from services import TaskService
from typing import Annotated
from schemas import TaskResponse
from dependecies import get_current_user, get_task_service
from config import settings
from exceptions import NotFoundException


router = APIRouter(tags=[settings.api.v1.task.tag])


@router.get(settings.api.v1.task.get_by_id, response_model=TaskResponse)
async def get_task_by_id(
        task_id: UUID,
        payload: Annotated[dict, Depends(get_current_user)],
        task_service: Annotated[TaskService, Depends(get_task_service)]
):
    """Получение упражнения по ID."""
    try:
        return await task_service.get_task(payload['role'], id=task_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.name))


@router.get(settings.api.v1.task.get_by_material, response_model=TaskResponse)
async def get_task_by_material(
        material_id: UUID,
        variant_id: UUID,
        task_number: int,
        payload: Annotated[dict, Depends(get_current_user)],
        task_service: Annotated[TaskService, Depends(get_task_service)]
):
    """Получение упражнения по учебному материалу."""
    try:
        return await task_service.get_task(
            payload['role'],
            material_id=material_id,
            variant_id=variant_id,
            number=task_number,
            is_study_task=True
        )
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.name))


@router.get(settings.api.v1.task.get_by_homework, response_model=TaskResponse)
async def get_task_by_homework(
        homework_id: UUID,
        task_number: int,
        payload: Annotated[dict, Depends(get_current_user)],
        task_service: Annotated[TaskService, Depends(get_task_service)]
):
    """Получение упражнения по домашнему заданию."""
    try:
        return await task_service.get_task_by_homework(
            payload['role'],
            homework_id=homework_id,
            task_number=task_number
        )
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.name))
