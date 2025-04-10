from sqlalchemy import select, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any, Sequence

from .abstract_repo import AbstractRepository


class SQLAlchemyRepository(AbstractRepository):
    """Абстрактный репозиторий для работы с SQLAlchemy ORM.

    :param db: Асинхронная сессия SQLAlchemy
    :var model: Модель SQLAlchemy, с которой работает репозиторий
    """

    model = None

    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_one(self, fields: List[str], **filter_by) -> RowMapping:
        """Получает одну запись, возвращая только указанные поля.

        :param fields: Список полей для выборки
        :param filter_by: Условия фильтрации (ключ - имя поля, значение - условие)

        :return: Данные записи или None, если не найдено
        """
        columns = [getattr(self.model, field) for field in fields]
        stmt = select(*columns).filter_by(**filter_by)
        res = await self.db.execute(stmt)
        return res.mappings().first()

    async def find_all(
            self,
            fields: List[str],
            filter_by: Optional[Dict[str, Any]] = None,
            order_by: Optional[str] = None,
            limit: Optional[int] = None
    ) -> Sequence[RowMapping]:
        """Получает все записи с поддержкой фильтрации, сортировки и ограничения количества.

        :param fields: Список полей для выборки
        :param filter_by: Условия фильтрации
        :param order_by: Поле для сортировки
        :param limit: Максимальное количество записей

        :return: Список записей
        """

        columns = [getattr(self.model, field) for field in fields]
        stmt = select(*columns)

        if filter_by:
            filters = [getattr(self.model, key) == value for key, value in filter_by.items()]
            stmt = stmt.where(*filters)

        if order_by:
            stmt = stmt.order_by(getattr(self.model, order_by))

        if limit:
            stmt = stmt.limit(limit)

        res = await self.db.execute(stmt)
        return res.mappings().all()
