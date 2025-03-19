from typing import List, Dict, Any

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
    settings: Dict[str, Any]


class VariantForActiveTask(PyBaseModel):
    variant_id: UUID
    name: str
    count: int


class VariantForLastTask(PyBaseModel):
    name: str
    student_mark: int
    max_mark: int
    tasks: List[TaskForLastHomework]


class VariantForTeacher(VariantForActiveTask):
    max_mark: int


class VariantForCreateTask(PyBaseModel):
    variant_id: UUID
    settings: Dict[str, Any]
