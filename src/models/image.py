from uuid import UUID, uuid4

import sqlalchemy as alchemy
from sqlalchemy import Text, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Image(Base):
    """Модель изображения"""
    __tablename__ = 'image'

    id: Mapped[UUID] = mapped_column(alchemy.UUID, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(length=50), nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)

    def __str__(self):
        return f'name = {self.name}'
