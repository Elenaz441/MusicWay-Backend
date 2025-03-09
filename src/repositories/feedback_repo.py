from .sqlalchemy_repo import SQLAlchemyRepository

from models import Feedback


class FeedbackRepository(SQLAlchemyRepository):
    """Репозиторий для обратной связи."""
    model = Feedback
