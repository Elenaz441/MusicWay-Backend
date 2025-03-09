from .sqlalchemy_repo import SQLAlchemyRepository
from models import Role


class RoleRepository(SQLAlchemyRepository):
    """Репозиторий для ролей."""
    model = Role
