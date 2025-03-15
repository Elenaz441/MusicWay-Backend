from sqlalchemy import select, RowMapping
from models import Variant, TaskType
from .sqlalchemy_repo import SQLAlchemyRepository
from typing import Sequence, List
from uuid import UUID


class VariantRepository(SQLAlchemyRepository):
    """Репозиторий для вариантов упражнений."""

    model = Variant

    async def find_all_by_block(self, block_id: UUID, fields: List[str]) -> Sequence[RowMapping]:
        columns = [getattr(self.model, field) for field in fields]
        stmt = select(*columns).join(TaskType).where(block_id == TaskType.block_id)
        res = await self.db.execute(stmt)
        return res.mappings().all()
