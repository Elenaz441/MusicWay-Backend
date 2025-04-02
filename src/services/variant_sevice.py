from repositories import VariantRepository, TaskTypeRepository
from schemas import ShortVariantResponse, VariantResponse
from exceptions import NotFoundException
from uuid import UUID
import httpx


class VariantService:
    """Сервис для работы с вариантами упражнений."""
    def __init__(self, variant_repo: VariantRepository, task_type_repo: TaskTypeRepository):
        self.variant_repo = variant_repo
        self.task_type_repo = task_type_repo

    async def get_variants_by_block(self, block_id: UUID) -> list[ShortVariantResponse]:
        variants = await self.variant_repo.find_all_by_block(block_id, ['id', 'name', 'image_url'])
        result = [ShortVariantResponse.model_validate(rec) for rec in variants]
        return result

    async def get_variant(self, variant_id: UUID, role: str) -> VariantResponse:
        variant = await self.variant_repo.find_one(
            ['id', 'name', 'image_url', 'student_description', 'teacher_description', 'demo_url'],
            {'id': variant_id}
        )
        if not variant:
            raise NotFoundException('вариант', 'id')
        variant_dict = dict(variant)
        variant_dict['description'] = variant.student_description if role == 'Ученик' else variant.teacher_description

        task_type_id = await self.variant_repo.find_one(['task_type_id'], {'id': variant.id})
        task_type_url = await self.task_type_repo.find_one(['service_url'], {'id': task_type_id.task_type_id})
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{task_type_url.service_url}/settings')
        variant_dict['settings'] = response.json()
        return VariantResponse.model_validate(variant_dict)
