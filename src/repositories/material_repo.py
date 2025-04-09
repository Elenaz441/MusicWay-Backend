from sqlalchemy import func, select, RowMapping
from models import StudyMaterial, Task, HomeworkTask
from .sqlalchemy_repo import SQLAlchemyRepository
from typing import List, Optional, Dict, Any, Sequence
from uuid import UUID
import sqlalchemy as alchemy


class MaterialRepository(SQLAlchemyRepository):
    """Репозиторий для работы с учебными материалами."""

    model = StudyMaterial

    async def find_all(
            self,
            fields: List[str],
            filter_by: Optional[Dict[str, Any]] = None,
            order_by: Optional[str] = None,
            limit: Optional[int] = None
    ) -> Sequence[RowMapping]:
        """Получает список учебных материалов с возможностью фильтрации и поиска.

        :param fields: Список полей для выборки
        :param filter_by: Условия фильтрации (ключ-значение)
        :param order_by: Поле для сортировки
        :param limit: Максимальное количество результатов

        :return: Список учебных материалов"""

        columns = [getattr(self.model, field) for field in fields]
        stmt = select(*columns)

        if filter_by:
            filters = []
            for key, value in filter_by.items():
                column = getattr(self.model, key)
                if key == 'search_vector':
                    filters.append(column.op('@@')(func.plainto_tsquery('russian', value)))
                else:
                    filters.append(getattr(self.model, key) == value)
            stmt = stmt.where(*filters)

        if order_by:
            stmt = stmt.order_by(getattr(self.model, order_by))

        if limit:
            stmt = stmt.limit(limit)

        res = await self.db.execute(stmt)
        return res.mappings().all()

    async def find_all_by_homework(self, homework_id: UUID) -> Sequence[RowMapping]:
        """Получает учебные материалы, связанные с конкретным домашним заданием.

        :param homework_id: Идентификатор домашнего задания

        :return: Список материалов с ID и названием"""
        stmt = (
            select(
                StudyMaterial.id,
                StudyMaterial.name
            )
            .join(Task, Task.material_id == StudyMaterial.id)
            .join(HomeworkTask, HomeworkTask.task_id == Task.id)
            .where(homework_id == HomeworkTask.homework_id)
            .order_by(StudyMaterial.block_id, StudyMaterial.number)
            .distinct()
        )

        res = await self.db.execute(stmt)
        return res.mappings().all()
