from uuid import UUID, uuid4

import sqlalchemy as alchemy
from sqlalchemy import Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .study_material import StudyMaterial


class Feedback(Base):
    __tablename__ = 'feedback'

    id: Mapped[UUID] = mapped_column(alchemy.UUID, primary_key=True, default=uuid4)
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    is_processed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    material_id: Mapped[UUID] = mapped_column(ForeignKey(StudyMaterial.id, ondelete='RESTRICT'), nullable=False)

    material: Mapped[StudyMaterial] = relationship(back_populates='comments')

    def __str__(self):
        return f'{self.__class__.__name__}(id={self.id}, comment={self.comment})'
