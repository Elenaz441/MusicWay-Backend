from .sqlalchemy_repo import SQLAlchemyRepository
from models import Setting


class SettingRepo(SQLAlchemyRepository):
    """Репозиторий для настроек"""
    model = Setting
