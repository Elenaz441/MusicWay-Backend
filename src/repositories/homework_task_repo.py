from .sqlalchemy_repo import SQLAlchemyRepository
from models import HomeworkTask


class HomeworkTaskRepository(SQLAlchemyRepository):
    """Репозиторий для упражнений."""
    model = HomeworkTask
