from uuid import UUID, uuid4

import sqlalchemy as alchemy
from sqlalchemy import Text, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY

from .base import Base


class Melody(Base):
    """Модель мелодии"""
    __tablename__ = 'melody'

    id: Mapped[UUID] = mapped_column(alchemy.UUID, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    notes: Mapped[list] = mapped_column(ARRAY(String(length=50)), nullable=False)
    intervals: Mapped[str] = mapped_column(ARRAY(String(length=50)), nullable=False)
    audio_url: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[str] = mapped_column(Text, nullable=False)
    query: Mapped[str] = mapped_column(String(length=50), nullable=False)

    def __str__(self):
        return f'name = {self.name}'
