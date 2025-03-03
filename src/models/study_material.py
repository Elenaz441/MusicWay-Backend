from uuid import UUID, uuid4

import sqlalchemy as alchemy
from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from storage import FileType
from .base import Base
from .topic_block import TopicBlock


class StudyMaterial(Base):
    __tablename__ = 'study_material'

    id: Mapped[UUID] = mapped_column(alchemy.UUID, primary_key=True, default=uuid4)
    topic_id: Mapped[UUID] = mapped_column(ForeignKey(TopicBlock.id, ondelete='RESTRICT'), nullable=False)
    name: Mapped[str] = mapped_column(String(length=100), unique=True, nullable=False)
    video_url: Mapped[str] = mapped_column(FileType, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)

    topic: Mapped[TopicBlock] = relationship(back_populates='materials')
    comments: Mapped[list['Feedback']] = relationship(back_populates='material')
    tasks: Mapped[list['Task']] = relationship(back_populates='material')

    def __str__(self):
        return self.name
