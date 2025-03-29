from uuid import UUID, uuid4

import sqlalchemy as alchemy
from sqlalchemy import Text, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY

from .base import Base


class Audio(Base):
    __tablename__ = 'audio'

    id: Mapped[UUID] = mapped_column(alchemy.UUID, primary_key=True, default=uuid4)
    notes: Mapped[list] = mapped_column(ARRAY(String(length=15)), nullable=False)
    interval: Mapped[str] = mapped_column(String(length=10), nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)

    def __str__(self):
        return f'interval = {self.interval}, notes = {self.notes}'
