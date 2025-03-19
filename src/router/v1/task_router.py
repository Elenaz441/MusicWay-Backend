from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from services import TaskService
from typing import Annotated
from schemas import TaskResponse, VariantForCreateTask, TaskAnswer, TaskSubmit
from dependecies import get_current_user, get_task_service
from exceptions import NotFoundException


router = APIRouter(tags=['Task'])


@router.post('', response_model=UUID)
async def create_task(
        data: VariantForCreateTask,
        payload: Annotated[dict, Depends(get_current_user)],
        task_service: Annotated[TaskService, Depends(get_task_service)]
):
    """Создание упражнения для тренажёра."""
    return await task_service.create_task(data)


@router.get('/{task_id}', response_model=TaskResponse)
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


@router.get('/{material_id}/{variant_id}/{task_number}', response_model=TaskResponse)
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


@router.get('/{homework_id}/{task_number}', response_model=TaskResponse)
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


@router.post('/{task_id}/check', response_model=TaskAnswer)
async def check_task(
        task_id: UUID,
        data: TaskSubmit,
        payload: Annotated[dict, Depends(get_current_user)],
        task_service: Annotated[TaskService, Depends(get_task_service)]
):
    try:
        return await task_service.check_task(task_id, data)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.name))

