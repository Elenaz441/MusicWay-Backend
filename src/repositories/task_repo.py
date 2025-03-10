from .sqlalchemy_repo import SQLAlchemyRepository
from models import Task, Variant
from typing import List, Optional, Dict, Any, Sequence, Type
from sqlalchemy import select, RowMapping, func


class TaskRepository(SQLAlchemyRepository):
    """Репозиторий для упражнений."""
    model = Task

    async def find_one(self, fields: List[str], filter_by: Optional[Dict[str, Any]] = None) -> RowMapping:
        """Получает одну запись, возвращая только указанные поля."""
        columns = [getattr(self.model, field) for field in fields]
        stmt = select(*columns)

        if filter_by:
            filters = []
            for key, value in filter_by.items():
                if key == 'task_ids':
                    filters.append(Task.id.in_(value))
                else:
                    column = getattr(self.model, key)
                    filters.append(column == value)
            stmt = stmt.where(*filters)

        res = await self.db.execute(stmt)
        return res.mappings().first()

    async def find_all(
            self,
            fields: List[str],
            filter_by: Optional[Dict[str, Any]] = None,
            order_by: Optional[str] = None,
            limit: Optional[int] = None,
            group_by: Optional[List[str]] = None
    ) -> Sequence[RowMapping]:
        """Получает все записи с поддержкой фильтрации, сортировки и ограничения количества."""

        join_required = False
        columns = []
        for field in fields:
            if field == 'count':
                columns.append(func.count(Task.id).label('count'))
            elif field == 'name':
                columns.append(Variant.name.label('name'))
                join_required = True
            else:
                columns.append(getattr(self.model, field))
        stmt = select(*columns)

        if join_required:
            stmt = stmt.join(Variant, Task.variant_id == Variant.id)

        if filter_by:
            filters = [getattr(self.model, key) == value for key, value in filter_by.items()]
            stmt = stmt.where(*filters)

        if group_by:
            group_columns = []
            for field in group_by:
                if field == 'name':
                    group_columns.append(Variant.name)
                else:
                    group_columns.append(getattr(self.model, field))
            stmt = stmt.group_by(*group_columns)

        if order_by:
            stmt = stmt.order_by(getattr(self.model, order_by))

        if limit:
            stmt = stmt.limit(limit)

        res = await self.db.execute(stmt)
        return res.mappings().all()
