from sqlalchemy import select
from models import Variant, TaskType
from .sqlalchemy_repo import SQLAlchemyRepository
from typing import List, Dict, Any
from uuid import UUID


class VariantRepository(SQLAlchemyRepository):
    """Репозиторий для вариантов упражнений."""

    model = Variant

    async def find_all_by_block(self, block_id: UUID, fields: List[str]) -> List[Dict[str, Any]]:
        """Получает варианты упражнений для указанного тематического блока.

        :param block_id: Идентификатор тематического блока
        :param fields: Список полей для выборки (None для всех полей)

        :return: Список вариантов с дополнительной информацией"""
        columns = [getattr(self.model, field) for field in fields]
        stmt = select(*columns).join(TaskType).where(block_id == TaskType.block_id)
        res = await self.db.execute(stmt)
        return [dict(row) for row in res.mappings().all()]
