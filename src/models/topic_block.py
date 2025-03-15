from uuid import UUID, uuid4

import sqlalchemy as alchemy
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from storage import FileType
from .base import Base


class TopicBlock(Base):
    __tablename__ = 'topic_block'

    id: Mapped[UUID] = mapped_column(alchemy.UUID, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    image_url: Mapped[str] = mapped_column(FileType, nullable=False)

    materials: Mapped[list['StudyMaterial']] = relationship(back_populates='block')
    task_types: Mapped[list['TaskType']] = relationship(back_populates='block')
    homeworks: Mapped[list['Homework']] = relationship(back_populates='block')

    def __str__(self):
        return self.name
