from repositories import VariantRepository
from schemas import ShortVariantResponse, VariantResponse
from exceptions import NotFoundException
from uuid import UUID


class VariantService:
    def __init__(self, variant_repo: VariantRepository):
        self.variant_repo = variant_repo

    async def get_variants_by_block(self, block_id: UUID) -> list[ShortVariantResponse]:
        variants = await self.variant_repo.get_variants_by_block(block_id)
        result = [ShortVariantResponse.model_validate(rec) for rec in variants]
        return result

    async def get_variant(self, variant_id: UUID, role: str) -> VariantResponse:
        variant = await self.variant_repo.get_variant_by_id(variant_id)
        if not variant:
            raise NotFoundException('вариант', 'id')
        variant_dict = variant.__dict__
        variant_dict['description'] = variant.student_description if role == 'Ученик' else variant.teacher_description
        variant_dict['settings'] = {}  # TODO поменять на запрос на сервер
        return VariantResponse.model_validate(variant_dict)
