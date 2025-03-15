from repositories import TaskRepository, VariantRepository, HomeworkTaskRepository
from uuid import UUID
from typing import List
from exceptions import NotFoundException
from schemas import TaskResponse
from models import Variant, HomeworkTask


class TaskService:
    """Сервис для работы с упражнениями."""

    def __init__(
            self,
            task_repo: TaskRepository,
            variant_repo: VariantRepository,
            hw_task_repo: HomeworkTaskRepository
    ):
        self.task_repo = task_repo
        self.variant_repo = variant_repo
        self.hw_task_repo = hw_task_repo

    async def get_task(self, role: str, **filter_by) -> TaskResponse:
        """Получает упражнение."""
        result = await self.task_repo.find_one(['id', 'variant_id', 'condition', 'content'], filter_by)
        if not result:
            raise NotFoundException('упражнение', 'параметрами')
        variant = await self.variant_repo.find_one(
            ['name', 'student_description', 'teacher_description'],
            {'id': result['variant_id']})
        description = variant.student_description if role == 'Ученик' else variant.teacher_description
        task = TaskResponse(
            id=result.id,
            condition=result.condition,
            content=result.content,
            task_type_variant=variant.name,
            description=description
        )
        return task

    async def get_task_by_homework(self, role: str,  homework_id: UUID, task_number: int) -> TaskResponse:
        """Получает упражнение в домашнем задании."""
        task_ids = await self.hw_task_repo.find_all(['task_id'], filter_by={'homework_id': homework_id})
        if not task_ids:
            raise NotFoundException('упражнение', 'homework_id')
        task_ids = [task_id.task_id for task_id in task_ids]
        result = await self.task_repo.find_one(
            ['id', 'variant_id', 'condition', 'content'],
            {'task_ids': task_ids, 'number': task_number})
        if not result:
            raise NotFoundException('упражнение', 'task_number')
        variant = await self.variant_repo.find_one(
            ['name', 'student_description', 'teacher_description'],
            {'id': result['variant_id']})
        description = variant.student_description if role == 'Ученик' else variant.teacher_description
        task = TaskResponse(
            id=result.id,
            condition=result.condition,
            content=result.content,
            task_type_variant=variant.name,
            description=description
        )
        return task
