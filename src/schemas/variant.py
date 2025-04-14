from typing import List, Dict, Any, Optional

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


class VariantForCreateTask(PyBaseModel):
    variant_id: UUID
    settings: Optional[Dict[str, Any]] = None


class VariantStatistic(PyBaseModel):
    name: str
    success_rate: int
