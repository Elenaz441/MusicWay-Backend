from repositories import VariantRepository, TaskTypeRepository
from schemas import ShortVariantResponse, VariantResponse
from exceptions import NotFoundException
from utils import send_query
from uuid import UUID
from typing import List


class VariantService:
    """Сервис для работы с вариантами упражнений."""
    def __init__(self, variant_repo: VariantRepository, task_type_repo: TaskTypeRepository):
        self.variant_repo = variant_repo
        self.task_type_repo = task_type_repo

    async def get_variants_by_block(self, block_id: UUID, role: str) -> List[ShortVariantResponse]:
        """Получает варианты упражнений для раздела.

        :param block_id: Идентификатор раздела.
        :param role: Роль пользователя.

        :return: Список с информацией по каждому варианту.
        """
        variants = await self.variant_repo.find_all_by_block(
            block_id,
            ['id', 'name', 'image_url', 'student_description', 'teacher_description', 'demo_url']
        )
        result = []
        for variant in variants:
            variant_dict = dict(variant)
            variant_dict['description'] = variant.student_description if role == 'Ученик' else variant.teacher_description
            result.append(ShortVariantResponse.model_validate(variant_dict))
        return result

    async def get_variant(self, variant_id: UUID, role: str) -> VariantResponse:
        """Получает информацию о конкретном варианте упражнения.

        :param variant_id: Идентификатор варианта.
        :param role: Роль пользователя.

        :return: Информация о варианте.

        :raises NotFoundException: Если указанный вариант не найден.
        """
        variant = await self.variant_repo.find_one(
            ['id', 'name'],
            {'id': variant_id}
        )
        if not variant:
            raise NotFoundException('вариант', 'id')
        variant_dict = dict(variant)

        task_type_id = await self.variant_repo.find_one(['task_type_id'], {'id': variant.id})
        task_type_url = await self.task_type_repo.find_one(['service_url'], {'id': task_type_id.task_type_id})
        response = await send_query('GET', f'{task_type_url.service_url}/settings?role={role}')
        variant_dict['settings'] = response
        return VariantResponse.model_validate(variant_dict)
