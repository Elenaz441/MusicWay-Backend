from typing import List

from .base import PyBaseModel
from .task import TaskForLastHomework
from uuid import UUID


class ShortVariantResponse(PyBaseModel):
    id: UUID
    name: str
    image_url: str


class VariantResponse(ShortVariantResponse):
    description: str
    demo_url: str
    settings: dict


class VariantForActiveTask(PyBaseModel):
    variant_id: UUID
    name: str
    count: int


class VariantForLastTask(PyBaseModel):
    name: str
    student_mark: int
    max_mark: int
    tasks: List[TaskForLastHomework]
