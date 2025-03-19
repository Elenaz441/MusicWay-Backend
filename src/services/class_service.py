from repositories import ClassRepository, StudentClassRepository, UserRepository, HomeworkRepository
from schemas import ShortClassResponse, ClassResponse, ShortLastHWTeacher
from exceptions import NoRightsException, NotFoundException
from typing import List
from uuid import UUID


class ClassService:
    """Сервис для работы с разделами."""
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
        if role != 'Преподаватель':
            raise NoRightsException()
        classes = await self.class_repo.find_all(
            ['id', 'class_number', 'week_day', 'class_time'],
            {'teacher_id': teacher_id}
        )
        return [ShortClassResponse.model_validate(c) for c in classes]

    async def get_class_by_id(self, class_id: UUID, teacher_id: UUID, role: str) -> ClassResponse:
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
        homeworks = await self.homework_repo.find_all_active(class_id)
        result = dict(learning_class)
        result['students'] = students
        result['active_homeworks'] = homeworks
        return ClassResponse.model_validate(result)

    async def get_last_homeworks(self, class_id: UUID, teacher_id: UUID, role: str) -> List[ShortLastHWTeacher]:
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
        tasks = await self.homework_repo.find_all_completed(class_id)
        return [ShortLastHWTeacher.model_validate(task) for task in tasks]


