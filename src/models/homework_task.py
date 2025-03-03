from uuid import UUID, uuid4

import sqlalchemy as alchemy
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .user import User
from .homework import Homework
from .task import Task


class HomeworkTask(Base):
    __tablename__ = 'homework_task'

    id: Mapped[UUID] = mapped_column(alchemy.UUID, primary_key=True, default=uuid4)
    student_id: Mapped[UUID] = mapped_column(ForeignKey(User.id, ondelete='RESTRICT'), nullable=False)
    homework_id: Mapped[UUID] = mapped_column(ForeignKey(Homework.id, ondelete='RESTRICT'), nullable=False)
    task_id: Mapped[UUID] = mapped_column(ForeignKey(Task.id, ondelete='RESTRICT'), nullable=False)
    mark: Mapped[str] = mapped_column(Integer, nullable=True)

    student: Mapped[User] = relationship(back_populates='tasks')
    homework: Mapped[Homework] = relationship(back_populates='tasks')
    task: Mapped[Task] = relationship(back_populates='homework_tasks')

    def __str__(self):
        return str(self.id)
