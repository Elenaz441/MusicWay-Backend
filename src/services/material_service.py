from repositories import AbstractRepository
from uuid import UUID
from typing import List
from exceptions import NotFoundException
from schemas import ShortMaterialResponse, MaterialVideoResponse, MaterialTextResponse


class MaterialService:
    """Сервис для работы с учебными материалами."""

    def __init__(self, repo: AbstractRepository):
        self.repo = repo

    async def get_materials_by_block(self, block_id: UUID) -> List[ShortMaterialResponse]:
        """Получает материалы по разделу."""
        materials = await self.repo.find_all(['id', 'name'], filter_by={'block_id': block_id})
        result = [ShortMaterialResponse.model_validate(rec) for rec in materials]
        return result

    async def get_video(self, material_id: UUID) -> MaterialVideoResponse:
        """Получает видео по ID."""
        result = await self.repo.find_one(['video_url'], id=material_id)
        if not result:
            raise NotFoundException('учебный материал', 'id')
        return MaterialVideoResponse(video_url=result['video_url'])

    async def get_text(self, material_id: UUID) -> MaterialTextResponse:
        """Получает текст по ID."""
        result = await self.repo.find_one(['text'], id=material_id)
        if not result:
            raise NotFoundException('учебный материал', 'id')
        return MaterialTextResponse(text=result['text'])

    async def search_materials(self, query: str, limit: int = 5) -> List[ShortMaterialResponse]:
        """Полнотекстовый поиск по учебным материалам."""
        materials = await self.repo.find_all(['id', 'name'], filter_by={'search_vector': query}, limit=limit)
        result = [ShortMaterialResponse.model_validate(rec) for rec in materials]
        return result

