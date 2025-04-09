from uuid import UUID, uuid4
from typing import List

import sqlalchemy as alchemy
from sqlalchemy import String, ForeignKey, Text, Index, func, Integer, event, Computed
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import TSVECTOR

from storage import FileType
from .base import Base
from .topic_block import TopicBlock


class StudyMaterial(Base):
    """Модель учебного материала."""
    __tablename__ = 'study_material'

    id: Mapped[UUID] = mapped_column(alchemy.UUID, primary_key=True, default=uuid4)
    block_id: Mapped[UUID] = mapped_column(ForeignKey(TopicBlock.id, ondelete='RESTRICT'), nullable=False)
    name: Mapped[str] = mapped_column(String(length=100), unique=True, nullable=False)
    video_url: Mapped[str] = mapped_column(FileType('materials'), nullable=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    number: Mapped[int] = mapped_column(Integer, nullable=False)

    block: Mapped[TopicBlock] = relationship(back_populates='materials')
    comments: Mapped[List['Feedback']] = relationship(back_populates='material')
    tasks: Mapped[List['Task']] = relationship(back_populates='material')

    search_vector: Mapped[str] = mapped_column(
        TSVECTOR,
        Computed("to_tsvector('russian', name || ' ' || text)", persisted=True)
    )

    __table_args__ = (
        Index('study_materials_search_idx', search_vector, postgresql_using='gin'),
    )

    def __str__(self):
        return self.name


# @event.listens_for(StudyMaterial, 'before_insert')
# @event.listens_for(StudyMaterial, 'before_update')
# def update_search_vector(mapper, connection, target):
#     """Автоматически обновляет search_vector перед сохранением."""
#     target.search_vector = func.to_tsvector('russian', f'{target.name} {target.text}')
