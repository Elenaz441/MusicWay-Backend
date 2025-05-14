from .sqlalchemy_repo import SQLAlchemyRepository
from models import Melody
from sqlalchemy import select, func
from typing import Optional, Dict, Any


class MelodyRepo(SQLAlchemyRepository):
    """Репозиторий для мелодии"""
    model = Melody

    async def find_random_melody(self, fields) -> Optional[Dict[str, Any]]:
        """Получает одну случайную запись, возвращая только указанные поля.

        :param fields: Список полей для выборки

        :return: Данные записи или None, если не найдено
        """
        columns = [getattr(self.model, field) for field in fields]
        stmt = select(*columns).order_by(func.random())
        res = await self.db.execute(stmt)
        row = res.mappings().first()
        return dict(row) if row else None
