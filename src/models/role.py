from uuid import UUID, uuid4
from typing import List

import sqlalchemy as alchemy
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Role(Base):
    """Модель роли."""
    __tablename__ = 'role'

    id: Mapped[UUID] = mapped_column(alchemy.UUID, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(length=50), unique=True, nullable=False)

    users: Mapped[List['User']] = relationship(back_populates='role')

    def __str__(self):
        return self.name
