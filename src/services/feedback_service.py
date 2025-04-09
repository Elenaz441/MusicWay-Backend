from repositories import MaterialRepository, FeedbackRepository
from schemas import CreateFeedback
from exceptions import NoRightsException, NotFoundException
from uuid import UUID


class FeedbackService:
    """Сервис для работы с обратной связью."""
    def __init__(self, feedback_repo: FeedbackRepository, material_repo: MaterialRepository):
        self.material_repo = material_repo
        self.feedback_repo = feedback_repo

    async def create_feedback(self, feedback: CreateFeedback, role_name: str) -> UUID:
        """Создание обратной связи. Доступно только преподавателям.

        :param feedback: Объект с данными обратной связи.
        :param role_name: Роль пользователя (только 'Преподаватель' имеет доступ).

        :return: Идентификатор созданной записи обратной связи.

        :raises NoRightsException: Если роль пользователя не 'Преподаватель'.
        :raises NotFoundException: Если указанный учебный материал не найден."""
        if role_name != 'Преподаватель':
            raise NoRightsException()
        if not await self.material_repo.find_one(['id'], {'id': feedback.material_id}):
            raise NotFoundException('учебный материал', 'id')
        new_feedback = {
            'material_id': feedback.material_id,
            'comment': feedback.comment
        }
        return await self.feedback_repo.add_one(new_feedback)
