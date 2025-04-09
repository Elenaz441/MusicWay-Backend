from uuid import UUID, uuid4

import sqlalchemy as alchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .user import User
from .learning_class import LearningClass


class StudentClass(Base):
    """Модель связи ученика и класса."""
    __tablename__ = 'student_class'

    id: Mapped[UUID] = mapped_column(alchemy.UUID, primary_key=True, default=uuid4)
    student_id: Mapped[UUID] = mapped_column(ForeignKey(User.id, ondelete='RESTRICT'), unique=True, nullable=False)
    class_id: Mapped[UUID] = mapped_column(ForeignKey(LearningClass.id, ondelete='RESTRICT'), nullable=False)

    student: Mapped[User] = relationship(back_populates='student_class')
    learning_class: Mapped[LearningClass] = relationship(back_populates='students')

    def __str__(self):
        return f'{self.__class__.__name__}(id={self.id}, student_id={self.student_id})'
