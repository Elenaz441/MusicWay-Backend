from repositories import MaterialRepository, TaskRepository
from uuid import UUID
from typing import List
from exceptions import NotFoundException
from schemas import ShortMaterialResponse, MaterialVideoResponse, MaterialTextResponse, VariantForActiveTask


class MaterialService:
    """Сервис для работы с учебными материалами."""

    def __init__(self, material_repo: MaterialRepository, task_repo: TaskRepository):
        self.material_repo = material_repo
        self.task_repo = task_repo

    async def get_materials_by_block(self, block_id: UUID) -> List[ShortMaterialResponse]:
        """Получает материалы по разделу.

        :param block_id: Идентификатор раздела.

        :return: Список материалов по данному разделу.
        """
        materials = await self.material_repo.find_all(
            ['id', 'name'],
            filter_by={'block_id': block_id},
            order_by='number'
        )
        result = [ShortMaterialResponse.model_validate(rec) for rec in materials]
        return result

    async def get_video(self, material_id: UUID) -> MaterialVideoResponse:
        """Получает видео по идентификатору.

        :param material_id: Идентификатор учебного материала.

        :return: Ссылка на видео.

        :raises NotFoundException: Если указанный материал не найден.
        """
        result = await self.material_repo.find_one(['video_url'], {'id': material_id})
        if not result:
            raise NotFoundException('учебный материал', 'id')
        return MaterialVideoResponse(video_url=result['video_url'])

    async def get_text(self, material_id: UUID) -> MaterialTextResponse:
        """Получает текст по идентификатору.

        :param material_id: Идентификатор учебного материала.

        :return: Текст учебного материала.

        :raises NotFoundException: Если указанный материал не найден.
        """
        result = await self.material_repo.find_one(['text'], {'id': material_id})
        if not result:
            raise NotFoundException('учебный материал', 'id')
        return MaterialTextResponse(text=result['text'])

    async def get_tasks(self, material_id: UUID) -> List[VariantForActiveTask]:
        """Получает задания, относящиеся к разделу

        :param material_id: Идентификатор учебного материала.

        :return: Список с количеством упражнений для каждого варианта.

        :raises NotFoundException: Если указанный материал не найден.
        """
        check = await self.material_repo.find_one(['id'], {'id': material_id})
        if not check:
            raise NotFoundException('учебный материал', 'id')
        tasks = await self.task_repo.find_all_by_material(material_id)
        tasks = [VariantForActiveTask.model_validate(task) for task in tasks]
        return tasks

    async def search_materials(self, query: str, limit: int = 5) -> List[ShortMaterialResponse]:
        """Полнотекстовый поиск по учебным материалам.

        :param query: Запрос, который пользователь ввел в поисковике.
        :param limit: Ограничение по количеству.

        :return: Список учебных материалов.
        """
        materials = await self.material_repo.find_all(['id', 'name'], filter_by={'search_vector': query}, limit=limit)
        result = [ShortMaterialResponse.model_validate(rec) for rec in materials]
        return result

