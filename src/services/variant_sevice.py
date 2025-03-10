from repositories import AbstractRepository
from schemas import ShortVariantResponse, VariantResponse
from exceptions import NotFoundException
from uuid import UUID


class VariantService:
    """Сервис для работы с вариантами упражнений."""
    def __init__(self, repo: AbstractRepository):
        self.repo = repo

    async def get_variants_by_block(self, block_id: UUID) -> list[ShortVariantResponse]:
        variants = await self.repo.find_all(['id', 'name', 'image_url'], {'block_id': block_id})
        result = [ShortVariantResponse.model_validate(rec) for rec in variants]
        return result

    async def get_variant(self, variant_id: UUID, role: str) -> VariantResponse:
        variant = await self.repo.find_one(
            ['id', 'name', 'image_url', 'student_description', 'teacher_description', 'demo_url'],
            {'id': variant_id})
        if not variant:
            raise NotFoundException('вариант', 'id')
        variant_dict = dict(variant)
        variant_dict['description'] = variant.student_description if role == 'Ученик' else variant.teacher_description
        variant_dict['settings'] = {}  # TODO поменять на запрос на сервер
        return VariantResponse.model_validate(variant_dict)
