from .base import PyBaseModel
from .variant import VariantForActiveTask
from uuid import UUID
from typing import Optional, List


class ShortMaterialResponse(PyBaseModel):
    id: UUID
    name: str
    number: int


class MaterialVideoResponse(PyBaseModel):
    name: str
    video_url: Optional[str] = None


class MaterialTextResponse(PyBaseModel):
    name: str
    text: str


class MaterialTasksResponse(PyBaseModel):
    name: str
    variants: List[VariantForActiveTask]
