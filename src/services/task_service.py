from repositories import TaskRepository, VariantRepository, HomeworkTaskRepository, TaskTypeRepository
from uuid import UUID
from utils import send_query
from exceptions import NotFoundException, NoRightsException
from schemas import TaskResponse, VariantForCreateTask, TaskSubmit, TaskAnswer
from typing import Any


class TaskService:
    """Сервис для работы с упражнениями."""

    def __init__(
            self,
            task_repo: TaskRepository,
            variant_repo: VariantRepository,
            hw_task_repo: HomeworkTaskRepository,
            task_type_repo: TaskTypeRepository,
    ):
        self.task_repo = task_repo
        self.variant_repo = variant_repo
        self.hw_task_repo = hw_task_repo
        self.task_type_repo = task_type_repo

    async def _take_task(self, task_info: Any, role: str) -> TaskResponse:
        """Собирает и дополняет информацию об упражнении.

        :param task_info: Информация об упражнении.
        :param role: Роль пользователя.

        :return: Дополненная информация об упражнении.
        """
        variant = await self.variant_repo.find_one(
            ['name', 'student_description', 'teacher_description'],
            {'id': task_info['variant_id']})
        description = variant.student_description if role == 'Ученик' else variant.teacher_description
        return TaskResponse(
            id=task_info.id,
            condition=task_info.condition,
            content=task_info.content,
            task_type_variant=variant.name,
            description=description
        )

    async def get_task(self, role: str, **filter_by) -> TaskResponse:
        """Получает упражнение.

        :param role: Роль пользователя.
        :param filter_by: Фильтры.

        :return: Информация об упражнении.

        :raises NotFoundException: Если указанное упражнение не найдено.
        """
        result = await self.task_repo.find_one(['id', 'variant_id', 'condition', 'content'], filter_by)
        if not result:
            raise NotFoundException('упражнение', 'параметрами')
        return await self._take_task(result, role)

    async def get_task_by_homework(self, role: str, homework_id: UUID, task_number: int) -> TaskResponse:
        """Получает упражнение в домашнем задании.

        :param role: Роль пользователя.
        :param homework_id: Идентификатор домашнего задания.
        :param task_number: Номер упражнения.

        :return: Информация об упражнении.

        :raises NotFoundException: Если указанное упражнение не найдено.
        :raises NoRightsException: Нет прав.
        """
        if role != 'Ученик':
            raise NoRightsException()
        task_ids = await self.hw_task_repo.find_all(['task_id'], filter_by={'homework_id': homework_id})
        if not task_ids:
            raise NotFoundException('упражнение', 'homework_id')
        task_ids = [task_id.task_id for task_id in task_ids]
        result = await self.task_repo.find_one(
            ['id', 'variant_id', 'condition', 'content'],
            {'task_ids': task_ids, 'number': task_number})
        if not result:
            raise NotFoundException('упражнение', 'task_number')
        return await self._take_task(result, role)

    async def create_task(self, data: VariantForCreateTask) -> UUID:
        """Создание упражнения для тренажёра.

        :param data: Данные для создания упражнения.

        :return: Идентификатор созданного упражнения.
        """
        task_type_id = await self.variant_repo.find_one(['task_type_id'], {'id': data.variant_id})
        task_type_url = await self.task_type_repo.find_one(['service_url'], {'id': task_type_id.task_type_id})
        response = await send_query(
            'POST',
            f'{task_type_url.service_url}/tasks',
            data.settings
        )
        task = response[0]
        new_task = {
            'condition': task['condition'],
            'content': task['content'],
            'answer': task['answer'],
            'max_mark': task['max_mark'],
            'variant_id': data.variant_id,
        }
        return await self.task_repo.add_one(new_task)

    async def check_task(self, task_id: UUID, data: TaskSubmit) -> TaskAnswer:
        """Проверка упражнения.

        :param task_id: Идентификатор упражнения.
        :param data: Данные об ответе пользователя.

        :return: Результат проверки упражнения.
        """
        task = await self.task_repo.find_one(
            ['id', 'answer', 'is_study_task', 'variant_id'],
            {'id': task_id}
        )
        if not task:
            raise NotFoundException('task', 'id')
        task_type_id = await self.variant_repo.find_one(['task_type_id'], {'id': task.variant_id})
        task_type_url = await self.task_type_repo.find_one(['service_url'], {'id': task_type_id.task_type_id})
        response = await send_query(
            'POST',
            f'{task_type_url.service_url}/tasks/check',
            {'check_data': data.check_data, 'answer': task.answer}
        )
        is_right = response['is_right']
        if not task.is_study_task and data.delete_it:
            await self.task_repo.delete_one(task_id)
        return TaskAnswer(is_right=is_right, answer=task.answer)
