from .sqlalchemy_repo import SQLAlchemyRepository
from models import Homework, Task, HomeworkTask, Variant, TopicBlock, User
from typing import Sequence, Optional, Dict, Any
from sqlalchemy import select, func, between, exists, RowMapping, Integer
from sqlalchemy.sql.functions import coalesce
from uuid import UUID
from datetime import datetime, timedelta


class HomeworkRepository(SQLAlchemyRepository):
    """Репозиторий для домашних заданий."""
    model = Homework

    async def find_one_with_mark(self, homework_id: UUID, student_id: UUID) -> RowMapping:
        """Получает домашнее задание с баллами студента.

        :param homework_id: Идентификатор домашнего задания
        :param student_id: Идентификатор ученика

        :return: Информация о домашнем задании с баллами или None
        """
        stmt = (
            select(
                Homework.id, Homework.topic,
                Homework.start_date, Homework.end_date, TopicBlock.name.label('block'),
                coalesce(func.sum(HomeworkTask.mark), 0).label('student_mark'),
                func.sum(Task.max_mark).label('max_mark'),
            )
            .join(HomeworkTask, HomeworkTask.homework_id == Homework.id)
            .join(Task, HomeworkTask.task_id == Task.id)
            .join(TopicBlock, Homework.block_id == TopicBlock.id)
            .where(homework_id == Homework.id, student_id == HomeworkTask.student_id)
            .group_by(Homework.id, TopicBlock.name)
        )

        res = await self.db.execute(stmt)
        return res.mappings().first()

    async def find_all_active(self, class_id: UUID, student_id: Optional[UUID] = None) -> Sequence[RowMapping]:
        """Получает активные домашние задания для класса.

        :param class_id: Идентификатор класса
        :param student_id: Опциональный идентификатор ученика

        :return: Список активных заданий
        """

        filter_by = [class_id == Homework.class_id, between(func.now(), Homework.start_date, Homework.end_date)]
        if student_id:
            filter_by.extend([
                exists().where(
                    HomeworkTask.homework_id == Homework.id,
                    student_id == HomeworkTask.student_id,
                    HomeworkTask.mark.is_(None)
                ).correlate(Homework),
                student_id == HomeworkTask.student_id
            ])

        stmt = (
            select(
                Homework.id, Homework.topic,
                Homework.start_date, Homework.end_date,
                func.sum(Task.max_mark).label('max_mark'),
                func.count(HomeworkTask.homework_id).label('count')
            )
            .join(HomeworkTask, HomeworkTask.homework_id == Homework.id)
            .join(Task, HomeworkTask.task_id == Task.id)
            .where(*filter_by)
            .group_by(Homework.id)
        )

        res = await self.db.execute(stmt)
        return res.mappings().all()

    async def find_all_completed(self, filter_by: Dict[str, Any]) -> Sequence[RowMapping]:
        """Получает завершенные домашние задания по фильтру.

        :param filter_by: Словарь условий фильтрации

        :return: Список завершенных заданий
        """
        filters = []
        student_condition = None
        for key, value in filter_by.items():
            if key == 'student_id':
                student_condition = ((Homework.end_date < func.now())
                                     | ~exists().where(
                                        HomeworkTask.homework_id == Homework.id,
                                        value == HomeworkTask.student_id,
                                        HomeworkTask.mark.is_(None)
                                    ).correlate(Homework))
                filters.extend([
                    student_condition,
                    value == HomeworkTask.student_id
                ])
            else:
                filters.append(getattr(self.model, key) == value)
        if student_condition is None:
            filters.append(Homework.end_date < func.now())

        stmt = (
            select(
                Homework.id, Homework.topic,
                coalesce(func.sum(HomeworkTask.mark), 0).label('student_mark'),
                func.sum(Task.max_mark).label('max_mark'),
            )
            .join(HomeworkTask, HomeworkTask.homework_id == Homework.id)
            .join(Task, HomeworkTask.task_id == Task.id)
            .where(*filters)
            .group_by(Homework.id)
        )

        res = await self.db.execute(stmt)
        return res.mappings().all()

    async def is_completed(self, homework_id: UUID, student_id: UUID) -> bool:
        """Проверяет, завершено ли домашнее задание.

        :param homework_id: Идентификатор задания
        :param student_id: Идентификатор ученика

        :return: True если задание завершено, иначе False
        """
        stmt = select(
            exists().where(
                homework_id == Homework.id,
                Homework.end_date < func.now()
            )
            | ~exists().where(
                homework_id == HomeworkTask.homework_id,
                student_id == HomeworkTask.student_id,
                HomeworkTask.mark.is_(None)
            )
        )
        res = await self.db.execute(stmt)
        return res.scalar()

    async def get_marks(self, homework_id: UUID, student_id: Optional[UUID] = None) -> Sequence[RowMapping]:
        """Получает оценки по домашнему заданию.

        :param homework_id: Идентификатор задания
        :param student_id: Опциональный идентификатор ученика

        :return: Список оценок
        """

        filter_by = [homework_id == HomeworkTask.homework_id]
        if student_id:
            filter_by.append(student_id == HomeworkTask.student_id)

        stmt = (
            select(
                Variant.name.label('name'),
                Task.number,
                func.coalesce(HomeworkTask.mark, 0).label('student_mark'),
                Task.max_mark
            )
            .join(Task, Task.variant_id == Variant.id)
            .join(HomeworkTask, HomeworkTask.task_id == Task.id)
            .where(*filter_by)
            .order_by(Task.number)
        )

        res = await self.db.execute(stmt)
        return res.mappings().all()

    async def get_homework_students(self, homework_id: UUID) -> Sequence[RowMapping]:
        """Получает список учеников с их баллами по заданию.

        :param homework_id: Идентификатор задания

        :return: Список учеников с баллами
        """
        stmt = (
            select(
                User.id,
                User.name,
                User.surname,
                User.patronymic,
                func.sum(HomeworkTask.mark).label('student_mark')
            )
            .join(HomeworkTask, HomeworkTask.student_id == User.id)
            .where(homework_id == HomeworkTask.homework_id)
            .group_by(User.id)
            .order_by(User.surname, User.name)
        )

        res = await self.db.execute(stmt)
        return res.mappings().all()

    async def get_homework_tasks(self, homework_id: UUID) -> Sequence[RowMapping]:
        """Получает детальную информацию по заданиям.

        :param homework_id: Идентификатор задания

        :return: Список заданий с оценками
        """
        stmt = (
            select(
                User.id.label('student_id'),
                Variant.name.label('task_name'),
                HomeworkTask.mark.label('student_mark'),
                Task.max_mark
            )
            .join(HomeworkTask, HomeworkTask.student_id == User.id)
            .join(Task, HomeworkTask.task_id == Task.id)
            .join(Variant, Task.variant_id == Variant.id)
            .where(homework_id == HomeworkTask.homework_id)
            .order_by(User.surname, User.name)
        )

        res = await self.db.execute(stmt)
        return res.mappings().all()

    async def get_statistic(self, class_id: UUID) -> Sequence[RowMapping]:
        """Получает статистику по завершенным заданиям за последние 3 месяца.

        :param class_id: Идентификатор класса

        :return: Статистика успеваемости
        """
        three_months_ago = datetime.now().date() - timedelta(days=90)

        stmt = (
            select(
                Homework.id,
                Homework.topic,
                func.round(
                    (
                        func.coalesce(func.sum(HomeworkTask.mark), 0) * 100 /
                        (func.sum(Task.max_mark))
                    ),
                    0
                ).cast(Integer).label('success_rate')
            )
            .join(HomeworkTask, HomeworkTask.homework_id == Homework.id, isouter=True)
            .join(Task, HomeworkTask.task_id == Task.id, isouter=True)
            .where(
                class_id == Homework.class_id,
                Homework.end_date >= three_months_ago,
                Homework.end_date < datetime.now().date()
            )
            .group_by(Homework.id)
            .order_by(Homework.end_date.desc())
        )

        res = await self.db.execute(stmt)
        return res.mappings().all()
