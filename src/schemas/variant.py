from .base import PyBaseModel
from uuid import UUID


class ShortVariantResponse(PyBaseModel):
    id: UUID
    name: str
    image_url: str


class VariantResponse(ShortVariantResponse):
    description: str
    demo_url: str
    settings: dict
