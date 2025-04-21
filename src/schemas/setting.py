from .base import PyBaseModel
from typing import List, Optional
from uuid import UUID


class MelodyResponse(PyBaseModel):
    id: UUID
    name: str


class MelodySettingResponse(PyBaseModel):
    description: Optional[str]
    melodies: Optional[List[MelodyResponse]]
    is_need_count: bool

