from fastapi import APIRouter, Depends

from services import TaskService
from typing import Annotated, List
from schemas import CreateTaskSetting, TaskResponse
from dependecies import get_task_service


router = APIRouter(tags=['Tasks'])


@router.post('', response_model=List[TaskResponse])
async def create_tasks(
        data: CreateTaskSetting,
        task_service: Annotated[TaskService, Depends(get_task_service)]
):
    """Создает упражнения."""
    return await task_service.create_task(data)
