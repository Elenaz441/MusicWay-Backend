from .sqlalchemy_repo import SQLAlchemyRepository
from models import User


class UserRepository(SQLAlchemyRepository):
    """Репозиторий для пользователей."""
    model = User
