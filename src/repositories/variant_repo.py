from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from models import Variant, TaskType


class VariantRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_variants_by_block(self, block_id: UUID):
        """Поиск вариантов по разделу."""
        result = await self.db.execute(
            select(Variant.id, Variant.name, Variant.image_url)
            .join(TaskType)
            .where(block_id == TaskType.block_id)
        )
        return result.mappings().all()

    async def get_variant_by_id(self, variant_id: UUID):
        """Получение информации о варианте задания по id"""
        result = await self.db.execute(select(Variant).where(variant_id == Variant.id))
        return result.scalars().first()
