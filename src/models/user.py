from uuid import UUID, uuid4
from datetime import datetime

import sqlalchemy as alchemy
from sqlalchemy import String, Text, Boolean, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .role import Role


class User(Base):
    """Модель пользователя."""
    __tablename__ = 'user'

    id: Mapped[UUID] = mapped_column(alchemy.UUID, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(length=100), nullable=False)
    surname: Mapped[str] = mapped_column(String(length=100), nullable=False)
    patronymic: Mapped[str] = mapped_column(String(length=100), nullable=True)
    birthdate: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    email: Mapped[str] = mapped_column(String(length=255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(Text, nullable=False)
    is_first_login: Mapped[bool] = mapped_column(Boolean, default=True)
    role_id: Mapped[UUID] = mapped_column(ForeignKey(Role.id, ondelete='RESTRICT'), nullable=False)

    role: Mapped[Role] = relationship(back_populates='users')
    classes: Mapped[list['LearningClass']] = relationship(back_populates='teacher')
    student_class: Mapped['StudentClass'] = relationship(back_populates='student')
    tasks: Mapped[list['HomeworkTask']] = relationship(back_populates='student')

    @property
    def full_name(self) -> str:
        return f'{self.surname} {self.name}'

    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic}'
