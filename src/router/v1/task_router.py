from fastapi import APIRouter, Depends, HTTPException, status

from services import TaskService
from typing import Annotated, List
from schemas import CreateTaskSetting, TaskResponse, CheckTask, CheckTaskResponse, GetMarkTaskResponse
from dependecies import get_task_service
from exceptions import NotFoundException


router = APIRouter(tags=['Tasks'])


@router.post('', response_model=List[TaskResponse])
async def create_tasks(
        data: CreateTaskSetting,
        task_service: Annotated[TaskService, Depends(get_task_service)]
):
    """Создает упражнения.

    :param data: Данные для создания упражнения.
    :param task_service: Сервис упражнений.

    :return: Список созданных упражнений.
    """
    try:
        return await task_service.create_task(data)
    except NotFoundException as e:
        raise HTTPException(detail=str(e.name), status_code=status.HTTP_404_NOT_FOUND)


@router.post('/check', response_model=CheckTaskResponse)
async def check_tasks(
        data: CheckTask,
        task_service: Annotated[TaskService, Depends(get_task_service)]
):
    """Проверяет правильно ли выполнено упражнение.

    :param data: Данные для проверки.
    :param task_service: Сервис упражнений.

    :return: Результат проверки.
    """
    try:
        return await task_service.check_task(data)
    except NotFoundException as e:
        raise HTTPException(detail=str(e.name), status_code=status.HTTP_404_NOT_FOUND)


@router.post('/get-mark', response_model=GetMarkTaskResponse)
async def get_mark(
        data: CheckTask,
        task_service: Annotated[TaskService, Depends(get_task_service)]
):
    """Выставляет балл за упражнение.

    :param data: Данные для проверки.
    :param task_service: Сервис упражнений.

    :return: Балл за упражнение.
    """
    try:
        return await task_service.get_mark(data)
    except NotFoundException as e:
        raise HTTPException(detail=str(e.name), status_code=status.HTTP_404_NOT_FOUND)
