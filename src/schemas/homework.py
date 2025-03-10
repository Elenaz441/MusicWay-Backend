from .base import PyBaseModel
from .variant import VariantForActiveTask, VariantForLastTask
from .material import ShortMaterialResponse
from datetime import date
from uuid import UUID
from typing import List


class ShortActiveHomework(PyBaseModel):
    id: UUID
    topic: str
    end_date: date
    max_mark: int


class ActiveHomework(ShortActiveHomework):
    task_type_variants: List[VariantForActiveTask]
    related_materials: List[ShortMaterialResponse]


class ShortLastHomework(PyBaseModel):
    id: UUID
    topic: str
    student_mark: int
    max_mark: int


class LastHomework(ShortLastHomework):
    task_type_variants: List[VariantForLastTask]
