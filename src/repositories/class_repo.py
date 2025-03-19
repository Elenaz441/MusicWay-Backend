from .sqlalchemy_repo import SQLAlchemyRepository

from models import LearningClass


class ClassRepository(SQLAlchemyRepository):
    """Репозиторий для классов."""
    model = LearningClass
