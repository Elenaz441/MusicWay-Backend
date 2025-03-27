from uuid import UUID, uuid4

import sqlalchemy as alchemy
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY

from .base import Base


class Setting(Base):
    __tablename__ = 'setting'

    id: Mapped[UUID] = mapped_column(alchemy.UUID, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(length=10), nullable=False)
    values: Mapped[list] = mapped_column(ARRAY(String(length=5)), nullable=False)

    def __str__(self):
        return f'name = {self.name}'
