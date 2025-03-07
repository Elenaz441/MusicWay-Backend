from .base import PyBaseModel
from uuid import UUID


class CreateFeedback(PyBaseModel):
    material_id: UUID
    comment: str
