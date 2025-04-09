from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from services import TaskService
from typing import Annotated, Dict
from schemas import TaskResponse, VariantForCreateTask, TaskAnswer, TaskSubmit
from dependecies import get_current_user, get_task_service
from exceptions import NotFoundException


router = APIRouter(tags=['Task'])


@router.post('', response_model=UUID)
async def create_task(
        data: VariantForCreateTask,
        payload: Annotated[Dict, Depends(get_current_user)],
        task_service: Annotated[TaskService, Depends(get_task_service)]
):
    """Создание упражнения для тренажёра.

    :param data: Данные о варианте для создания упражнения
    :param payload: JWT payload текущего пользователя.
    :param task_service: Сервис для работы с упражнениями.

    :return: Идентификатор нового упражнения.
    """
    return await task_service.create_task(data)


@router.get('/{task_id}', response_model=TaskResponse)
async def get_task_by_id(
        task_id: UUID,
        payload: Annotated[Dict, Depends(get_current_user)],
        task_service: Annotated[TaskService, Depends(get_task_service)]
):
    """Получение упражнения по идентификатору.

    :param task_id: Идентификатор упражнения.
    :param payload: JWT payload текущего пользователя.
    :param task_service: Сервис для работы с упражнениями.

    :return: Информация об упражнении.

    :raises HTTPException 404: Упражнение не найдено.
    """
    try:
        return await task_service.get_task(payload['role'], id=task_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.name))


@router.get('/{material_id}/{variant_id}/{task_number}', response_model=TaskResponse)
async def get_task_by_material(
        material_id: UUID,
        variant_id: UUID,
        task_number: int,
        payload: Annotated[Dict, Depends(get_current_user)],
        task_service: Annotated[TaskService, Depends(get_task_service)]
):
    """Получение упражнения по учебному материалу.

    :param material_id: Идентификатор материала.
    :param variant_id: Идентификатор варианта.
    :param task_number: Номер упражнения.
    :param payload: JWT payload текущего пользователя.
    :param task_service: Сервис для работы с упражнениями.

    :return: Информация об упражнении.

    :raises HTTPException 404: Упражнение не найдено.
    """
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
        payload: Annotated[Dict, Depends(get_current_user)],
        task_service: Annotated[TaskService, Depends(get_task_service)]
):
    """Получение упражнения по домашнему заданию.

    :param homework_id: Идентификатор задания.
    :param task_number: Номер упражнения.
    :param payload: JWT payload текущего пользователя.
    :param task_service: Сервис для работы с упражнениями.

    :return: Информация об упражнении.

    :raises HTTPException 404: Упражнение не найдено.
    """
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
        payload: Annotated[Dict, Depends(get_current_user)],
        task_service: Annotated[TaskService, Depends(get_task_service)]
):
    """Отправка упражнения на проверку.

    :param task_id: Идентификатор упражнения.
    :param data: Данные ответа.
    :param payload: JWT payload текущего пользователя.
    :param task_service: Сервис для работы с упражнениями.

    :return: Результат проверки.

    :raises HTTPException 404: Упражнение не найдено.
    """
    try:
        return await task_service.check_task(task_id, data)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.name))

