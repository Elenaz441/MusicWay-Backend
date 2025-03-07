from .base import PyBaseModel
from uuid import UUID


class TopicBlockResponse(PyBaseModel):
    id: UUID
    name: str
    image_url: str
