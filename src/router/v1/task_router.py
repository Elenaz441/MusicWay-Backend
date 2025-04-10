from fastapi import APIRouter, Depends

from services import TaskService
from typing import Annotated, List
from schemas import CreateTaskSetting, TaskResponse, CheckTask, CheckTaskResponse, GetMarkTaskResponse
from dependecies import get_task_service


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
    return await task_service.create_task(data)


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
    return await task_service.check_task(data)


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
    return await task_service.get_mark(data)
