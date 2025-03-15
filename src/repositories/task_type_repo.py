from models import TaskType
from .sqlalchemy_repo import SQLAlchemyRepository


class TaskTypeRepository(SQLAlchemyRepository):
    """Репозиторий для типов заданий."""
    model = TaskType
