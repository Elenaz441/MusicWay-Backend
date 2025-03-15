from models import StudentClass
from .sqlalchemy_repo import SQLAlchemyRepository


class StudentClassRepository(SQLAlchemyRepository):
    """Репозиторий для StudentClass."""
    model = StudentClass
