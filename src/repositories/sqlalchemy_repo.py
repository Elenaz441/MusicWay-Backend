from uuid import UUID
from sqlalchemy import insert, select, update, delete, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any, Sequence, Type

from .abstract_repo import AbstractRepository


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_one(self, data: Dict) -> UUID:
        """Добавляет новую запись"""
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await self.db.execute(stmt)
        await self.db.commit()
        return res.scalar_one()

    async def edit_one(self, id: UUID, data: Dict) -> UUID:
        """Изменяет запись по переданному id"""
        stmt = update(self.model).values(**data).filter_by(id=id).returning(self.model.id)
        res = await self.db.execute(stmt)
        await self.db.commit()
        return res.scalar_one()

    async def delete_one(self, id: UUID) -> UUID:
        """Удаляет запись по переданному id"""
        stmt = delete(self.model).filter_by(id=id).returning(self.model.id)
        res = await self.db.execute(stmt)
        await self.db.commit()
        return res.scalar_one()

    async def find_one(self, fields: List[str], filter_by: Optional[Dict[str, Any]] = None) -> RowMapping:
        """Получает одну запись, возвращая только указанные поля."""
        columns = [getattr(self.model, field) for field in fields]
        stmt = select(*columns)

        if filter_by:
            filters = [getattr(self.model, key) == value for key, value in filter_by.items()]
            stmt = stmt.where(*filters)

        res = await self.db.execute(stmt)
        return res.mappings().first()

    async def find_all(
            self,
            fields: List[str],
            filter_by: Optional[Dict[str, Any]] = None,
            order_by: Optional[str] = None,
            limit: Optional[int] = None,
            group_by: Optional[List[str]] = None
    ) -> Sequence[RowMapping]:
        """Получает все записи с поддержкой фильтрации, сортировки и ограничения количества."""

        columns = [getattr(self.model, field) for field in fields]
        stmt = select(*columns)

        if filter_by:
            filters = [getattr(self.model, key) == value for key, value in filter_by.items()]
            stmt = stmt.where(*filters)

        if group_by:
            group_columns = [getattr(self.model, field) for field in group_by]
            stmt = stmt.group_by(*group_columns)

        if order_by:
            stmt = stmt.order_by(getattr(self.model, order_by))

        if limit:
            stmt = stmt.limit(limit)

        res = await self.db.execute(stmt)
        return res.mappings().all()
