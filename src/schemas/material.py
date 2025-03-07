from .base import PyBaseModel
from uuid import UUID


class ShortMaterialResponse(PyBaseModel):
    id: UUID
    name: str


class MaterialVideoResponse(PyBaseModel):
    video_url: str


class MaterialTextResponse(PyBaseModel):
    text: str
