from .sqlalchemy_repo import SQLAlchemyRepository
from models import Task, Variant, HomeworkTask
from typing import List, Optional, Dict, Any, Sequence
from sqlalchemy import select, RowMapping, func
from uuid import UUID


class TaskRepository(SQLAlchemyRepository):
    """Репозиторий для упражнений."""
    model = Task

    async def find_one(self, fields: List[str], filter_by: Optional[Dict[str, Any]] = None) -> RowMapping:
        """Получает одно задание с указанными полями.

        :param fields: Список полей для выборки
        :param filter_by: Условия фильтрации (может включать список ID заданий)

        :return: Данные задания или None, если не найдено"""
        columns = [getattr(self.model, field) for field in fields]
        stmt = select(*columns)

        if filter_by:
            filters = []
            for key, value in filter_by.items():
                if key == 'task_ids':
                    filters.append(Task.id.in_(value))
                else:
                    filters.append(getattr(self.model, key) == value)
            stmt = stmt.where(*filters)

        res = await self.db.execute(stmt)
        return res.mappings().first()

    async def find_all_by_material(self, material_id: UUID) -> Sequence[RowMapping]:
        """Возвращает количество упражнений, сгруппированных по варианту, для учебного материала.

        :param material_id: Идентификатор учебного материала

        :return: Список вариантов с количеством заданий"""

        stmt = (
            select(
                Task.variant_id.label('variant_id'),
                Variant.name.label('name'),
                func.count(Task.id).label('count')
            )
            .join(Variant, Task.variant_id == Variant.id)
            .where(material_id == Task.material_id, Task.is_study_task)
            .group_by(Task.variant_id, Variant.name)
        )

        res = await self.db.execute(stmt)
        return res.mappings().all()

    async def find_all_by_homework(self, homework_id: UUID, student_id: UUID) -> Sequence[RowMapping]:
        """Получает задания домашней работы с группировкой по вариантам.

        :param homework_id: Идентификатор домашней работы
        :param student_id: Идентификатор ученика

        :return: Список вариантов с количеством заданий"""
        stmt = (
            select(
                Variant.id.label('variant_id'),
                Variant.name,
                func.count(Task.id).label('count'),
            )
            .join(Task, Task.variant_id == Variant.id)
            .join(HomeworkTask, HomeworkTask.task_id == Task.id)
            .where(homework_id == HomeworkTask.homework_id, student_id == HomeworkTask.student_id)
            .group_by(Variant.id)
        )

        res = await self.db.execute(stmt)
        return res.mappings().all()
