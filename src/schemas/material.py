from .base import PyBaseModel
from uuid import UUID
from typing import Optional


class ShortMaterialResponse(PyBaseModel):
    id: UUID
    name: str


class MaterialVideoResponse(PyBaseModel):
    video_url: Optional[str] = None


class MaterialTextResponse(PyBaseModel):
    text: str
