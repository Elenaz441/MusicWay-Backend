from .sqlalchemy_repo import SQLAlchemyRepository
from models import Audio


class AudioRepo(SQLAlchemyRepository):
    """Репозиторий для аудиозаписей"""
    model = Audio
