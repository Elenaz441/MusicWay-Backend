from repositories import FeedbackRepository, MaterialRepository
from schemas import CreateFeedback
from models import Feedback
from exceptions import NoRightsException, NotFoundException


class FeedbackService:
    def __init__(self, feedback_repo: FeedbackRepository, material_repo: MaterialRepository):
        self.material_repo = material_repo
        self.feedback_repo = feedback_repo

    async def create_feedback(self, feedback: CreateFeedback, role_name: str) -> Feedback:
        """Создание обратной связи."""
        if role_name != 'Преподаватель':
            raise NoRightsException()
        if not await self.material_repo.get_video(feedback.material_id):
            raise NotFoundException('учебный материал', 'id')
        new_feedback = Feedback(
            material_id=feedback.material_id,
            comment=feedback.comment
        )
        return await self.feedback_repo.create_feedback(new_feedback)
