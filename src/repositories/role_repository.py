from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from models import Role


class RoleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_role_by_name(self, name: str) -> Optional[Role]:
        """Поиск роли по названию."""
        result = await self.db.execute(select(Role).where(Role.name == name))
        return result.scalars().first()

    async def get_role_by_id(self, id: str) -> Optional[Role]:
        """Поиск роли по id."""
        result = await self.db.execute(select(Role).where(Role.id == id))
        return result.scalars().first()
