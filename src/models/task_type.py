from uuid import UUID, uuid4

import sqlalchemy as alchemy
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .topic_block import TopicBlock


class TaskType(Base):
    __tablename__ = 'task_type'

    id: Mapped[UUID] = mapped_column(alchemy.UUID, primary_key=True, default=uuid4)
    block_id: Mapped[UUID] = mapped_column(ForeignKey(TopicBlock.id, ondelete='RESTRICT'), nullable=False)
    name: Mapped[str] = mapped_column(String(length=100), unique=True, nullable=False)

    block: Mapped[TopicBlock] = relationship(back_populates='task_types')
    variants: Mapped[list['Variant']] = relationship(back_populates='task_type')

    def __str__(self):
        return self.name
