from uuid import UUID, uuid4

import sqlalchemy as alchemy
from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from storage import FileType
from .base import Base
from .task_type import TaskType


class Variant(Base):
    __tablename__ = 'variant'

    id: Mapped[UUID] = mapped_column(alchemy.UUID, primary_key=True, default=uuid4)
    task_type_id: Mapped[UUID] = mapped_column(ForeignKey(TaskType.id, ondelete='RESTRICT'), nullable=False)
    name: Mapped[str] = mapped_column(String(length=100), unique=True, nullable=False)
    student_description: Mapped[str] = mapped_column(Text, nullable=False)
    teacher_description: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[str] = mapped_column(FileType, nullable=False)
    demo_url: Mapped[str] = mapped_column(FileType, nullable=False)

    task_type: Mapped[TaskType] = relationship(back_populates='variants')
    tasks: Mapped[list['Task']] = relationship(back_populates='variant')

    def __str__(self):
        return self.name
