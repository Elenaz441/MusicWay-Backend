from sqlalchemy import select, RowMapping
from models import Variant, TaskType
from .sqlalchemy_repo import SQLAlchemyRepository
from typing import Any, Sequence, List, Optional, Dict


class VariantRepository(SQLAlchemyRepository):
    """Репозиторий для вариантов упражнений."""

    model = Variant

    async def find_all(
            self,
            fields: List[str],
            filter_by: Optional[Dict[str, Any]] = None,
            order_by: Optional[str] = None,
            limit: Optional[int] = None
    ) -> Sequence[RowMapping]:
        """Получает все записи с поддержкой фильтрации, сортировки и ограничения количества."""

        columns = [getattr(self.model, field) for field in fields]
        stmt = select(*columns).join(TaskType).where(TaskType.block_id == filter_by['block_id'])

        if order_by:
            stmt = stmt.order_by(getattr(self.model, order_by))

        if limit:
            stmt = stmt.limit(limit)

        res = await self.db.execute(stmt)
        return res.mappings().all()
