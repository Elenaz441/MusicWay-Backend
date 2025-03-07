from repositories import MaterialRepository
from schemas import ShortMaterialResponse, MaterialVideoResponse, MaterialTextResponse
from exceptions import NotFoundException
from uuid import UUID


class MaterialService:
    def __init__(self, material_repo: MaterialRepository):
        self.material_repo = material_repo

    async def get_materials(self, block_id: UUID) -> list[ShortMaterialResponse]:
        materials = await self.material_repo.get_materials_by_block(block_id)
        result = [ShortMaterialResponse.model_validate(rec) for rec in materials]
        return result

    async def get_video(self, material_id: UUID) -> MaterialVideoResponse:
        video_url = await self.material_repo.get_video(material_id)
        if not video_url:
            raise NotFoundException('учебный материал', 'id')
        return MaterialVideoResponse(video_url=video_url)

    async def get_text(self, material_id: UUID) -> MaterialTextResponse:
        text = await self.material_repo.get_text(material_id)
        if not text:
            raise NotFoundException('учебный материал', 'id')
        return MaterialTextResponse(text=text)

    async def search_materials(self, query: str) -> list[ShortMaterialResponse]:
        materials = await self.material_repo.search_materials(query)
        result = [ShortMaterialResponse.model_validate(rec) for rec in materials]
        return result

