from repositories import (
    TopicBlockRepository,
    StudentClassRepository,
    HomeworkRepository,
    VariantRepository
)
from schemas import TopicBlockResponse, VariantStatistic
from exceptions import NoRightsException, NotFoundException
from utils import calculate_statistic
from typing import List
from uuid import UUID


class TopicBlockService:
    """Сервис для работы с разделами."""
    def __init__(
            self,
            block_repo: TopicBlockRepository,
            student_class_repo: StudentClassRepository,
            homework_repo: HomeworkRepository,
            variant_repo: VariantRepository
    ):
        self.block_repo = block_repo
        self.student_class_repo = student_class_repo
        self.homework_repo = homework_repo
        self.variant_repo = variant_repo

    async def get_blocks(self) -> List[TopicBlockResponse]:
        """Получает все разделы.

        :return: Список разделов.
        """
        blocks = await self.block_repo.find_all(['id', 'name', 'image_url'])
        result = [TopicBlockResponse.model_validate(rec) for rec in blocks]
        return result

    async def get_statistic(self, block_id: UUID, user_id: UUID, role: str) -> List[VariantStatistic]:
        """Получает статистику по разделу.

        :param block_id: Идентификатор раздела.
        :param user_id: Идентификатор пользователя.
        :param role: Роль пользователя.

        :return: Список со статистикой по каждому варианту упражнения.

        :raises NoRightsException: Нет прав.
        """
        if role != 'Ученик':
            raise NoRightsException()

        class_id = await self.student_class_repo.find_one(['class_id'], {'student_id': user_id})
        if not class_id:
            raise NotFoundException('класс', 'user_id')
        homeworks = await self.homework_repo.find_all_completed(
            {'class_id': class_id.class_id, 'student_id': user_id, 'block_id': block_id}
        )
        variants = await self.variant_repo.find_all_by_block(block_id, ['name'])
        result = {}
        for hw in homeworks:
            hw_tasks = await self.homework_repo.get_marks(hw.id, user_id)
            result = calculate_statistic(hw_tasks, result)

        for variant in variants:
            if variant.name not in result:
                result[variant.name] = {'name': variant.name, 'student_mark': 0, 'max_mark': 1}

        return [
            VariantStatistic(
                name=r['name'],
                success_rate=r['student_mark'] * 100 // r['max_mark']
            )
            for r in result.values()
        ]
