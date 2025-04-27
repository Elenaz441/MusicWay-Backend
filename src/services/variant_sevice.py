from repositories import VariantRepository, TaskTypeRepository, TopicBlockRepository
from schemas import ShortVariantResponse, VariantListResponse, VariantResponse
from exceptions import NotFoundException
from utils import send_query
from uuid import UUID
from typing import List, Optional


class VariantService:
    """Сервис для работы с вариантами упражнений."""
    def __init__(self, variant_repo: VariantRepository, task_type_repo: TaskTypeRepository, block_repo: TopicBlockRepository):
        self.variant_repo = variant_repo
        self.task_type_repo = task_type_repo
        self.block_repo = block_repo

    async def get_variants_by_block(self, block_id: Optional[UUID], role: str) -> List[VariantListResponse]:
        """Получает варианты упражнений для раздела.

        :param block_id: Идентификатор раздела.
        :param role: Роль пользователя.

        :return: Список с информацией по каждому варианту.
        """
        if block_id is None:
            blocks = await self.block_repo.find_all(['id', 'name'])
        else:
            blocks = [await self.block_repo.find_one(['id', 'name'], {'id': block_id})]
        result = []
        for block in blocks:
            variants = await self.variant_repo.find_all_by_block(
                block.id,
                ['id', 'name', 'image_url', 'student_description', 'teacher_description', 'demo_url']
            )
            variant_list = []
            for variant in variants:
                variant_dict = dict(variant)
                variant_dict['description'] = variant.student_description if role == 'Ученик' else variant.teacher_description
                variant_list.append(ShortVariantResponse.model_validate(variant_dict))
            result.append(VariantListResponse(block_name=block.name, variants=variant_list))
        return result

    async def get_variant(self, variant_id: UUID, role: str) -> VariantResponse:
        """Получает информацию о конкретном варианте упражнения.

        :param variant_id: Идентификатор варианта.
        :param role: Роль пользователя.

        :return: Информация о варианте.

        :raises NotFoundException: Если указанный вариант не найден.
        """
        variant = await self.variant_repo.find_one(
            ['id', 'name', 'student_description', 'teacher_description', 'demo_url'],
            {'id': variant_id}
        )
        if not variant:
            raise NotFoundException('вариант', 'id')
        variant_dict = dict(variant)

        task_type_id = await self.variant_repo.find_one(['task_type_id'], {'id': variant.id})
        task_type_url = await self.task_type_repo.find_one(['service_url'], {'id': task_type_id.task_type_id})
        response = await send_query('GET', f'{task_type_url.service_url}/settings?role={role}')
        variant_dict['description'] = variant.student_description if role == 'Ученик' else variant.teacher_description
        variant_dict['settings'] = response
        return VariantResponse.model_validate(variant_dict)
