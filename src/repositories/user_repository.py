from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from models import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Поиск пользователя по email."""
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def create_user(self, user: User) -> User:
        """Создание нового пользователя."""
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def change_user_password(self, user: User, new_password: str) -> User:
        user.hashed_password = new_password
        await self.db.commit()
        return user

    async def change_user_is_first_login(self, user: User) -> User:
        user.is_first_login = False
        await self.db.commit()
        return user
