from uuid import UUID, uuid4
from datetime import datetime
from typing import List

import sqlalchemy as alchemy
from sqlalchemy import String, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .learning_class import LearningClass
from .topic_block import TopicBlock


class Homework(Base):
    """Модель домашнего задания."""
    __tablename__ = 'homework'

    id: Mapped[UUID] = mapped_column(alchemy.UUID, primary_key=True, default=uuid4)
    topic: Mapped[str] = mapped_column(String(100), nullable=False)
    start_date: Mapped[datetime.date] = mapped_column(Date, nullable=False, default=datetime.now)
    end_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    class_id: Mapped[UUID] = mapped_column(ForeignKey(LearningClass.id, ondelete='RESTRICT'), nullable=False)
    block_id: Mapped[UUID] = mapped_column(ForeignKey(TopicBlock.id), nullable=False)

    learning_class: Mapped[LearningClass] = relationship(back_populates='homeworks')
    block: Mapped[TopicBlock] = relationship(back_populates='homeworks')
    tasks: Mapped[List['HomeworkTask']] = relationship(back_populates='homework', passive_deletes=True)

    def __str__(self):
        return f'{self.__class__.__name__}(id={self.id}, topic={self.topic})'
