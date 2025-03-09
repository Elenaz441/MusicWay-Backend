from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from uuid import UUID

from models import StudyMaterial


class MaterialRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_materials_by_block(self, block_id: UUID):
        """Поиск материалов по разделу."""
        result = await self.db.execute(select(StudyMaterial.name, StudyMaterial.id).where(
            block_id == StudyMaterial.block_id))
        return result.mappings().all()

    async def get_video(self, material_id: UUID):
        """Получение ссылки на видео из учебного материала"""
        result = await self.db.execute(select(StudyMaterial.video_url).where(material_id == StudyMaterial.id))
        return result.scalars().first()

    async def get_text(self, material_id: UUID):
        """Получение текста из учебного материала"""
        result = await self.db.execute(select(StudyMaterial.text).where(material_id == StudyMaterial.id))
        return result.scalars().first()

    async def search_materials(self, query: str):
        """Полнотекстовый поиск по материалам."""
        stmt = select(StudyMaterial).where(
            StudyMaterial.search_vector.op('@@')(func.to_tsquery('russian', query))
        ).limit(5)
        result = await self.db.execute(stmt)
        return result.scalars().all()
