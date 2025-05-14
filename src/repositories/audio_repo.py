from .sqlalchemy_repo import SQLAlchemyRepository
from models import Audio
from sqlalchemy import select, func
from typing import Optional, Dict, Any


class AudioRepo(SQLAlchemyRepository):
    """Репозиторий для аудиозаписей"""
    model = Audio

    async def find_random_audio(self, fields, **filter_by) -> Optional[Dict[str, Any]]:
        """Получает одну случайную запись, возвращая только указанные поля.

        :param fields: Список полей для выборки
        :param filter_by: Условия фильтрации (ключ - имя поля, значение - условие)

        :return: Данные записи или None, если не найдено
        """
        columns = [getattr(self.model, field) for field in fields]
        stmt = select(*columns).filter_by(**filter_by).order_by(func.random())
        res = await self.db.execute(stmt)
        row = res.mappings().first()
        return dict(row) if row else None

