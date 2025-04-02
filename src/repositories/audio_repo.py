from .sqlalchemy_repo import SQLAlchemyRepository
from models import Audio
from sqlalchemy import select, RowMapping, func


class AudioRepo(SQLAlchemyRepository):
    """Репозиторий для аудиозаписей"""
    model = Audio

    async def find_random_audio(self, fields, **filter_by) -> RowMapping:
        """Получает одну запись, возвращая только указанные поля."""
        columns = [getattr(self.model, field) for field in fields]
        stmt = select(*columns).filter_by(**filter_by).order_by(func.random())
        res = await self.db.execute(stmt)
        return res.mappings().first()

