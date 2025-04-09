from uuid import UUID, uuid4

import sqlalchemy as alchemy
from sqlalchemy import Boolean, ForeignKey, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from .base import Base
from .variant import Variant
from .study_material import StudyMaterial


class Task(Base):
    """Модель упражнения."""
    __tablename__ = 'task'

    id: Mapped[UUID] = mapped_column(alchemy.UUID, primary_key=True, default=uuid4)
    variant_id: Mapped[UUID] = mapped_column(ForeignKey(Variant.id, ondelete='RESTRICT'), nullable=False)
    material_id: Mapped[UUID] = mapped_column(ForeignKey(StudyMaterial.id, ondelete='RESTRICT'), nullable=True)
    condition: Mapped[str] = mapped_column(Text, nullable=False)
    content: Mapped[dict] = mapped_column(JSONB, nullable=False)
    answer: Mapped[dict] = mapped_column(JSONB, nullable=False)
    number: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    max_mark: Mapped[int] = mapped_column(Integer, nullable=False)
    is_study_task: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    variant: Mapped[Variant] = relationship(back_populates='tasks')
    material: Mapped[StudyMaterial] = relationship(back_populates='tasks')
    homework_tasks: Mapped[list['HomeworkTask']] = relationship(back_populates='task')

    def __str__(self):
        return str(self.id)
