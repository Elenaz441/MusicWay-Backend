from repositories import (
    HomeworkRepository,
    StudentClassRepository,
    TaskRepository,
    MaterialRepository,
    TaskTypeRepository,
    VariantRepository,
    HomeworkTaskRepository
)
from uuid import UUID
from utils import send_query, calculate_statistic
from datetime import datetime, timezone
from typing import List, Union
from exceptions import NotFoundException, NoRightsException, IncorrectDataException
from schemas import ShortActiveHomework, ShortLastHomework, ActiveHomework, LastHomework, TeacherHomework, \
    CreateHomework, EditHomework, TaskHomeworkSubmit, VariantStatistic


class HomeworkService:
    """Сервис для работы с учебными материалами."""

    def __init__(
            self,
            homework_repo: HomeworkRepository,
            student_class_repo: StudentClassRepository,
            task_repo: TaskRepository,
            material_repo: MaterialRepository,
            task_type_repo: TaskTypeRepository,
            variant_repo: VariantRepository,
            hw_task_repo: HomeworkTaskRepository,
    ):
        self.homework_repo = homework_repo
        self.student_class_repo = student_class_repo
        self.task_repo = task_repo
        self.material_repo = material_repo
        self.task_type_repo = task_type_repo
        self.variant_repo = variant_repo
        self.hw_task_repo = hw_task_repo

    async def get_homeworks_by_user(
            self,
            user_id: UUID,
            active: bool
    ) -> List[Union[ShortActiveHomework, ShortLastHomework]]:
        """Получение списка домашних заданий.

        :param user_id: Идентификатор пользователя.
        :param active: Флаг, обозначающий какие задания вернуть (активные или завершенные).

        :return: Список домашних заданий.

        :raises NotFoundException: Если не найден класс для данного пользователя.
        """
        class_id = await self.student_class_repo.find_one(['class_id'], {'student_id': user_id})
        if not class_id:
            raise NotFoundException('класс', 'user_id')
        if active:
            tasks = await self.homework_repo.find_all_active(class_id.class_id, user_id)
            return [ShortActiveHomework.model_validate(task) for task in tasks]
        tasks = await self.homework_repo.find_all_completed({'class_id': class_id.class_id, 'student_id': user_id})
        return [ShortLastHomework.model_validate(task) for task in tasks]

    async def get_active_homework(self, homework_id: UUID, user_id: UUID, role: str) -> ActiveHomework:
        """Возвращает информацию для активного ДЗ ученику.

        :param homework_id: Идентификатор домашнего задания.
        :param user_id: Идентификатор пользователя.
        :param role: Роль пользователя.

        :return: Информация об активном домашнем задании.

        :raises NoRightsException: Нет прав.
        :raises IncorrectDataException: Задание уже завершено.
        :raises NotFoundException: Если указанное домашнее задание не найдено.
        """
        if role != 'Ученик':
            raise NoRightsException()

        is_completed = await self.homework_repo.is_completed(homework_id, user_id)
        if is_completed:
            raise IncorrectDataException('Задание уже завершено.')

        homework_info = await self.homework_repo.find_one_with_mark(homework_id, user_id)
        if not homework_info:
            raise NotFoundException('homework', 'homework_id')

        tasks = await self.task_repo.find_all_by_homework(homework_id, user_id)
        related_materials = await self.material_repo.find_all_by_homework(homework_id)

        result = dict(homework_info)
        result['task_type_variants'] = tasks
        result['related_materials'] = related_materials
        return ActiveHomework.model_validate(result)

    async def get_completed_homework(self, homework_id: UUID, user_id: UUID, role: str) -> LastHomework:
        """Возвращает информацию для завершенного ДЗ ученику.

        :param homework_id: Идентификатор домашнего задания.
        :param user_id: Идентификатор пользователя.
        :param role: Роль пользователя.

        :return: Информация о завершенном домашнем задании.

        :raises NoRightsException: Нет прав.
        :raises IncorrectDataException: Задание ещё не завершено.
        :raises NotFoundException: Если указанное домашнее задание не найдено.
        """
        if role != 'Ученик':
            raise NoRightsException()

        is_completed = await self.homework_repo.is_completed(homework_id, user_id)
        if not is_completed:
            raise IncorrectDataException('Задание ещё не завершено.')

        homework_info = await self.homework_repo.find_one_with_mark(homework_id, user_id)
        if not homework_info:
            raise NotFoundException('homework', 'homework_id')

        tasks = await self.homework_repo.get_marks(homework_id, user_id)
        grouped_tasks = {}
        for task in tasks:
            key = task['name']
            if key not in grouped_tasks:
                grouped_tasks[key] = {'name': key, 'student_mark': 0, 'max_mark': 0, 'tasks': []}
            grouped_tasks[key]['tasks'].append({
                'number': task['number'],
                'student_mark': task['student_mark'],
                'max_mark': task['max_mark']
            })
            grouped_tasks[key]['student_mark'] += task['student_mark']
            grouped_tasks[key]['max_mark'] += task['max_mark']

        result = dict(homework_info)
        result['task_type_variants'] = list(grouped_tasks.values())

        return LastHomework.model_validate(result)

    async def get_homework(self, homework_id: UUID, role: str) -> TeacherHomework:
        """Возвращает информацию о ДЗ для преподавателя.

        :param homework_id: Идентификатор домашнего задания.
        :param role: Роль пользователя.

        :return: Информация о домашнем задании.

        :raises NoRightsException: Нет прав.
        :raises NotFoundException: Если указанное домашнее задание не найдено.
        """
        if role != 'Преподаватель':
            raise NoRightsException()

        students = await self.homework_repo.get_homework_students(homework_id)
        homework_info = await self.homework_repo.find_one_with_mark(homework_id, students[0].id)
        if not homework_info:
            raise NotFoundException('homework', 'homework_id')

        is_completed = homework_info.end_date <= datetime.date(datetime.now(timezone.utc))

        task_type_variants = await self.task_repo.find_all_by_homework(homework_id, students[0].id)
        related_materials = await self.material_repo.find_all_by_homework(homework_id)
        tasks = await self.homework_repo.get_homework_tasks(homework_id)

        student_dict = {s['id']: {**s, 'tasks': {}} for s in students}

        for task in tasks:
            student_id = task['student_id']
            task_name = task['task_name']

            if task_name not in student_dict[student_id]['tasks']:
                student_dict[student_id]['tasks'][task_name] = {
                    'name': task_name,
                    'student_mark': None,
                    'max_mark': 0
                }

            student_mark = task['student_mark']
            if student_mark is not None:
                if student_dict[student_id]['tasks'][task_name]['student_mark'] is None:
                    student_dict[student_id]['tasks'][task_name]['student_mark'] = student_mark
                else:
                    student_dict[student_id]['tasks'][task_name]['student_mark'] += student_mark
            student_dict[student_id]['tasks'][task_name]['max_mark'] += task['max_mark']

        for student in student_dict.values():
            student['tasks'] = list(student['tasks'].values())

        result = dict(homework_info)
        result['is_completed'] = is_completed
        result['task_type_variants'] = task_type_variants
        result['related_materials'] = related_materials
        result['results'] = list(student_dict.values())
        return TeacherHomework.model_validate(result)

    async def create_homework(self, homework: CreateHomework, role: str) -> UUID:
        """Создание ДЗ.

        :param homework: Данные о новом домашнем задании.
        :param role: Роль пользователя.

        :return: Идентификатор созданного задания.

        :raises NoRightsException: Нет прав.
        """
        if role != 'Преподаватель':
            raise NoRightsException()
        new_homework = {
            'topic': homework.topic,
            'start_date': homework.start_date,
            'end_date': homework.end_date,
            'block_id': homework.block_id,
            'class_id': homework.class_id
        }

        task_ids = []
        number = 1

        for variant in homework.variants:
            task_type_id = await self.variant_repo.find_one(['task_type_id'], {'id': variant.variant_id})
            task_type_url = await self.task_type_repo.find_one(['service_url'], {'id': task_type_id.task_type_id})
            tasks = await send_query(
                'POST',
                f'{task_type_url.service_url}/tasks',
                variant.settings
            )
            for task in tasks:
                material_id = await self.material_repo.find_all(
                    ['id'],
                    filter_by={'search_vector': task['query']},
                    limit=1
                )
                new_task = {
                    'condition': task['condition'],
                    'content': task['content'],
                    'answer': task['answer'],
                    'max_mark': task['max_mark'],
                    'variant_id': variant.variant_id,
                    'material_id': material_id[0].id,
                    'number': number
                }
                task_id = await self.task_repo.add_one(new_task)
                task_ids.append(task_id)
                number += 1

        student_ids = await self.student_class_repo.find_all(['student_id'], {'class_id': homework.class_id})
        homework_id = await self.homework_repo.add_one(new_homework)
        for student_id in student_ids:
            for task_id in task_ids:
                homework_task = {
                    'student_id': student_id.student_id,
                    'homework_id': homework_id,
                    'task_id': task_id,
                }
                await self.hw_task_repo.add_one(homework_task)

        return homework_id

    async def edit_homework(self, homework_id: UUID, homework: EditHomework, role: str) -> UUID:
        """Редактирование ДЗ.

        :param homework_id: Идентификатор домашнего задания.
        :param homework: Данные, которые надо отредактировать.
        :param role: Роль пользователя.

        :return: Идентификатор отредактированного задания.

        :raises NoRightsException: Нет прав.
        """
        if role != 'Преподаватель':
            raise NoRightsException()
        await self.homework_repo.edit_one(homework_id, homework.model_dump(exclude_none=True))
        return homework_id

    async def delete_homework(self, homework_id: UUID, role: str):
        """Удаление ДЗ.

        :param homework_id: Идентификатор домашнего задания.
        :param role: Роль пользователя.

        :raises NoRightsException: Нет прав.
        """
        if role != 'Преподаватель':
            raise NoRightsException()
        task_ids = await self.hw_task_repo.find_all(['task_id'], {'homework_id': homework_id})
        await self.homework_repo.delete_one(homework_id)
        unique_task_ids = {task_id.task_id for task_id in task_ids}
        for task_id in unique_task_ids:
            await self.task_repo.delete_one(task_id)

    async def submit_homework(
            self,
            homework_id: UUID,
            tasks: List[TaskHomeworkSubmit],
            user_id: UUID,
            role: str
    ) -> LastHomework:
        """Отправка ДЗ на проверку.

        :param homework_id: Идентификатор домашнего задания.
        :param tasks: Данные об ответах ученика.
        :param user_id: Идентификатор пользователя.
        :param role: Роль пользователя.

        :return: Данные о завершенном домашнем задании.

        :raises NoRightsException: Нет прав.
        :raises NotFoundException: Если указанное домашнее задание не найдено.
        """
        if role != 'Ученик':
            raise NoRightsException()
        homework = await self.homework_repo.find_one(['id'], {'id': homework_id})
        if not homework:
            raise NotFoundException('homework', 'homework_id')
        for task_answer in tasks:
            task = await self.task_repo.find_one(['id', 'variant_id', 'answer'], {'id': task_answer.task_id})
            task_type_id = await self.variant_repo.find_one(['task_type_id'], {'id': task.variant_id})
            task_type_url = await self.task_type_repo.find_one(['service_url'], {'id': task_type_id.task_type_id})
            response = await send_query(
                'POST',
                f'{task_type_url.service_url}/tasks/get-mark',
                {'check_data': task_answer.check_data, 'answer': task.answer}
            )
            mark = response['mark']
            hw_task = await self.hw_task_repo.find_one(
                ['id'],
                {'homework_id': homework_id, 'student_id': user_id, 'task_id': task.id}
            )
            await self.hw_task_repo.edit_one(hw_task.id, {'mark': mark})
        return await self.get_completed_homework(homework_id, user_id, role)

    async def get_statistic(self, homework_id: UUID, role: str) -> List[VariantStatistic]:
        """Получение статистики по домашнему заданию.

        :param homework_id: Идентификатор домашнего задания.
        :param role: Роль пользователя.

        :return: Список статистики по каждому варианту упражнений.

        :raises NoRightsException: Нет прав.
        """
        if role != 'Преподаватель':
            raise NoRightsException()
        hw_tasks = await self.homework_repo.get_marks(homework_id)
        result = calculate_statistic(hw_tasks)

        return [
            VariantStatistic(
                name=r['name'],
                success_rate=r['student_mark'] * 100 // r['max_mark']
            )
            for r in result.values()
        ]
