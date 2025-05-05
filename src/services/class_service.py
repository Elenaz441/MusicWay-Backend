from repositories import ClassRepository, StudentClassRepository, UserRepository, HomeworkRepository
from schemas import ShortClassResponse, ClassResponse, ShortLastHWTeacher, HomeworkStatistic
from exceptions import NoRightsException, NotFoundException
from typing import List
from uuid import UUID


class ClassService:
    """Сервис для работы с классами."""
    def __init__(
            self,
            class_repo: ClassRepository,
            students_repo: StudentClassRepository,
            user_repo: UserRepository,
            homework_repo: HomeworkRepository
    ):
        self.class_repo = class_repo
        self.students_repo = students_repo
        self.user_repo = user_repo
        self.homework_repo = homework_repo

    async def get_classes(self, teacher_id: UUID, role: str) -> List[ShortClassResponse]:
        """Получение всех классов, прикреплённых к преподавателю.

        :param teacher_id: Идентификатор преподавателя.
        :param role: Роль пользователя (должна быть "Преподаватель").

        :return: Список краткой информации о классах.

        :raises NoRightsException: Если роль не соответствует требуемой.
        """
        if role != 'Преподаватель':
            raise NoRightsException()
        classes = await self.class_repo.find_all(
            ['id', 'class_number', 'week_day', 'class_time'],
            {'teacher_id': teacher_id}
        )
        return [ShortClassResponse.model_validate(c) for c in classes]

    async def get_class_by_id(self, class_id: UUID, teacher_id: UUID, role: str) -> ClassResponse:
        """Получение подробной информации о конкретном классе.

        :param class_id: Идентификатор класса.
        :param teacher_id: Идентификатор преподавателя.
        :param role: Роль пользователя (должна быть "Преподаватель").

        :return: Объект с полной информацией о классе.

        :raises NoRightsException: Если пользователь не имеет прав.
        :raises NotFoundException: Если класс не найден."""
        if role != 'Преподаватель':
            raise NoRightsException()
        learning_class = await self.class_repo.find_one(
            ['id', 'class_number', 'week_day', 'class_time', 'teacher_id'],
            {'id': class_id}
        )
        if learning_class is None:
            raise NotFoundException('class', 'id')
        if learning_class.teacher_id != teacher_id:
            raise NoRightsException()
        student_ids = await self.students_repo.find_all(['student_id'], {'class_id': class_id})
        students = [
            await self.user_repo.find_one(
                ['id', 'name', 'surname', 'patronymic'],
                {'id': s.student_id}
            ) for s in student_ids
        ]
        if len(students) == 0:
            homeworks = []
        else:
            homeworks = await self.homework_repo.find_all_active(class_id, students[0].id)
        result = dict(learning_class)
        result['students'] = students
        result['active_homeworks'] = homeworks
        return ClassResponse.model_validate(result)

    async def get_last_homeworks(self, class_id: UUID, teacher_id: UUID, role: str) -> List[ShortLastHWTeacher]:
        """Получение списка завершённых домашних заданий для класса.

        :param class_id: Идентификатор класса.
        :param teacher_id: Идентификатор преподавателя.
        :param role: Роль пользователя (должна быть "Преподаватель").

        :return: Список завершённых заданий.

        :raises NoRightsException: Если нет прав.
        :raises NotFoundException: Если класс не найден.
        """
        if role != 'Преподаватель':
            raise NoRightsException()
        learning_class = await self.class_repo.find_one(
            ['teacher_id'],
            {'id': class_id}
        )
        if learning_class is None:
            raise NotFoundException('class', 'id')
        if learning_class.teacher_id != teacher_id:
            raise NoRightsException()
        tasks = await self.homework_repo.find_all_completed({'class_id': class_id})
        return [ShortLastHWTeacher.model_validate(task) for task in tasks]

    async def get_statistic(self, class_id: UUID, role: str) -> List[HomeworkStatistic]:
        """Получение статистики выполнения домашних заданий за последние 3 месяца.

        :param class_id: Идентификатор класса.
        :param role: Роль пользователя (должна быть "Преподаватель").

        :return: Список статистики по домашним заданиям.

        :raises NoRightsException: Если роль не соответствует.
        """
        if role != 'Преподаватель':
            raise NoRightsException()
        statistics = await self.homework_repo.get_statistic(class_id)
        return [HomeworkStatistic.model_validate(statistic) for statistic in statistics]
