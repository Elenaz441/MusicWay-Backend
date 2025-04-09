from uuid import UUID
from sqlalchemy import insert, select, update, delete, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any, Sequence
from sqlalchemy.sql import Select

from .abstract_repo import AbstractRepository


class SQLAlchemyRepository(AbstractRepository):
    """Абстрактный репозиторий для работы с SQLAlchemy ORM.

    Предоставляет базовые CRUD-операции для моделей SQLAlchemy в асинхронном режиме.

    :param db: Асинхронная сессия SQLAlchemy
    :var model: Модель SQLAlchemy, с которой работает репозиторий
    """

    model = None

    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_one(self, data: Dict[str, Any]) -> UUID:
        """Добавляет новую запись в базу данных.

        :param data: Данные для вставки

        :return: UUID созданной записи

        :raises sqlalchemy.exc.SQLAlchemyError: При ошибках базы данных
        """
        stmt = insert(self.model).values(**data).returning(self.model.id)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalar_one()

    async def edit_one(self, id: UUID, data: Dict[str, Any]) -> UUID:
        """Обновляет существующую запись.

        :param id: Идентификатор записи
        :param data: Данные для обновления

        :return: UUID обновленной записи

        :raises sqlalchemy.exc.NoResultFound: Если запись не найдена
        """
        stmt = (update(self.model)
                .values(**data)
                .filter_by(id=id)
                .returning(self.model.id))
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalar_one()

    async def delete_one(self, id: UUID) -> UUID:
        """Удаляет запись из базы данных.

        :param id: Идентификатор записи для удаления

        :return: UUID удаленной записи

        :raises sqlalchemy.exc.NoResultFound: Если запись не найдена
        """
        stmt = (delete(self.model)
                .filter_by(id=id)
                .returning(self.model.id))
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalar_one()

    async def find_one(
            self,
            fields: List[str],
            filter_by: Optional[Dict[str, Any]] = None
    ) -> Optional[RowMapping]:
        """Возвращает одну запись с указанными полями.

        :param fields: Список полей для выборки
        :param filter_by: Условия фильтрации (ключ - имя поля, значение - условие)

        :return: Данные записи или None, если не найдено
        """
        stmt = self._build_select_query(fields, filter_by)
        result = await self.db.execute(stmt)
        return result.mappings().first()

    async def find_all(
            self,
            fields: List[str],
            filter_by: Optional[Dict[str, Any]] = None,
            order_by: Optional[str] = None,
            limit: Optional[int] = None
    ) -> Sequence[RowMapping]:
        """Возвращает список записей с возможностью фильтрации и сортировки.

        :param fields: Список полей для выборки
        :param filter_by: Условия фильтрации
        :param order_by: Поле для сортировки
        :param limit: Максимальное количество записей

        :return: Список записей
        """
        stmt = self._build_select_query(fields, filter_by, order_by, limit)
        result = await self.db.execute(stmt)
        return result.mappings().all()

    def _build_select_query(
            self,
            fields: List[str],
            filter_by: Optional[Dict[str, Any]] = None,
            order_by: Optional[str] = None,
            limit: Optional[int] = None
    ) -> Select:
        """Строит SQL-запрос для выборки данных.

        :param fields: Список полей для выборки
        :param filter_by: Условия фильтрации
        :param order_by: Поле для сортировки
        :param limit: Лимит записей

        :return: Построенный SQL-запрос
        """
        columns = [getattr(self.model, field) for field in fields]
        stmt = select(*columns)

        if filter_by:
            filters = [getattr(self.model, key) == value
                       for key, value in filter_by.items()]
            stmt = stmt.where(*filters)

        if order_by:
            stmt = stmt.order_by(getattr(self.model, order_by))

        if limit is not None:
            stmt = stmt.limit(limit)

        return stmt
