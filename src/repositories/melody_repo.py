from .sqlalchemy_repo import SQLAlchemyRepository
from models import Melody
from sqlalchemy import select, RowMapping, func


class MelodyRepo(SQLAlchemyRepository):
    """Репозиторий для мелодии"""
    model = Melody

    async def find_random_melody(self, fields) -> RowMapping:
        """Получает одну случайную запись, возвращая только указанные поля.

        :param fields: Список полей для выборки

        :return: Данные записи или None, если не найдено
        """
        columns = [getattr(self.model, field) for field in fields]
        stmt = select(*columns).order_by(func.random())
        res = await self.db.execute(stmt)
        return res.mappings().first()
