from sqlalchemy import func, select, RowMapping
from models import StudyMaterial, Task, HomeworkTask
from .sqlalchemy_repo import SQLAlchemyRepository
from typing import List, Optional, Dict, Any, Sequence
from uuid import UUID


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
        """Получает все записи с поддержкой фильтрации, сортировки и ограничения количества."""

        columns = [getattr(self.model, field) for field in fields]
        stmt = select(*columns)

        if filter_by:
            filters = []
            for key, value in filter_by.items():
                column = getattr(self.model, key)
                if key == 'search_vector':
                    filters.append(column.op('@@')(func.plainto_tsquery('russian', value)))
                else:
                    filters.append(column == value)
            stmt = stmt.where(*filters)

        if order_by:
            stmt = stmt.order_by(getattr(self.model, order_by))

        if limit:
            stmt = stmt.limit(limit)

        res = await self.db.execute(stmt)
        return res.mappings().all()

    async def find_all_by_homework(self, homework_id: UUID) -> Sequence[RowMapping]:
        """Получает связанные учебные материалы по заданиям."""
        stmt = (
            select(
                StudyMaterial.id,
                StudyMaterial.name
            )
            .join(Task, Task.material_id == StudyMaterial.id)
            .join(HomeworkTask, HomeworkTask.task_id == Task.id)
            .where(homework_id == HomeworkTask.homework_id)
            .distinct()
        )

        res = await self.db.execute(stmt)
        return res.mappings().all()
