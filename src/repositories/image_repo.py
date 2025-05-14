from .sqlalchemy_repo import SQLAlchemyRepository
from models import Image
from sqlalchemy import select, func
from typing import List, Dict, Any


class ImageRepo(SQLAlchemyRepository):
    """Репозиторий для изображений"""
    model = Image

    async def find_random_image(self, fields, limit=1) -> List[Dict[str, Any]]:
        """Получает несколько случайных записей, возвращая только указанные поля.

        :param fields: Список полей для выборки
        :param limit: Количество записей.

        :return: Данные записи или None, если не найдено
        """
        columns = [getattr(self.model, field) for field in fields]
        stmt = select(*columns).order_by(func.random()).limit(limit)
        res = await self.db.execute(stmt)
        return [dict(row) for row in res.mappings().all()]
