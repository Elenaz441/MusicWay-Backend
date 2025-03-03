from uuid import UUID, uuid4
from datetime import time

import sqlalchemy as alchemy
from sqlalchemy import Integer, ForeignKey, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .user import User
from .base import Base


class LearningClass(Base):
    __tablename__ = 'learning_class'

    id: Mapped[UUID] = mapped_column(alchemy.UUID, primary_key=True, default=uuid4)
    class_number: Mapped[str] = mapped_column(Integer, nullable=False)
    week_day: Mapped[str] = mapped_column(String(length=20), nullable=False, default='Понедельник')
    class_time: Mapped[time] = mapped_column(Time, nullable=False)
    teacher_id: Mapped[UUID] = mapped_column(ForeignKey(User.id, ondelete='RESTRICT'), nullable=False)

    teacher: Mapped[User] = relationship(back_populates='classes')
    students: Mapped[list['StudentClass']] = relationship(back_populates='learning_class')
    homeworks: Mapped[list['Homework']] = relationship(back_populates='learning_class')

    def __str__(self):
        return f'Класс {self.class_number}. {self.week_day} в {self.class_time}'
