from .sqlalchemy_repo import SQLAlchemyRepository
from models import Homework


class HomeworkRepository(SQLAlchemyRepository):
    """Репозиторий для домашних заданий."""
    model = Homework
