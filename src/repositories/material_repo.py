from sqlalchemy import func, select, RowMapping
from models import StudyMaterial
from .sqlalchemy_repo import SQLAlchemyRepository
from typing import List, Optional, Dict, Any, Sequence


class MaterialRepository(SQLAlchemyRepository):
    """Репозиторий для работы с учебными материалами."""

    model = StudyMaterial

    async def find_all(
            self,
            fields: List[str],
            filter_by: Optional[Dict[str, Any]] = None,
            order_by: Optional[str] = None,
            limit: Optional[int] = None,
            group_by: Optional[List[str]] = None
    ) -> Sequence[RowMapping]:
        """Получает все записи с поддержкой фильтрации, сортировки и ограничения количества."""

        columns = [getattr(self.model, field) for field in fields]
        stmt = select(*columns)

        if filter_by:
            filters = []
            for key, value in filter_by.items():
                column = getattr(self.model, key)
                if key == 'search_vector':
                    filters.append(column.op('@@')(func.to_tsquery('russian', value)))
                else:
                    filters.append(column == value)
            stmt = stmt.where(*filters)

        if group_by:
            group_columns = [getattr(self.model, field) for field in group_by]
            stmt = stmt.group_by(*group_columns)

        if order_by:
            stmt = stmt.order_by(getattr(self.model, order_by))

        if limit:
            stmt = stmt.limit(limit)

        res = await self.db.execute(stmt)
        return res.mappings().all()
