from .base import PyBaseModel
from .variant import VariantForActiveTask, VariantForLastTask, VariantForTeacher, VariantForCreateTask
from .material import ShortMaterialResponse
from .user import UserResultTask
from datetime import date
from uuid import UUID
from typing import List, Optional


class ShortActiveHomework(PyBaseModel):
    id: UUID
    topic: str
    start_date: date
    end_date: date
    max_mark: int


class ActiveHomework(ShortActiveHomework):
    block: str
    task_type_variants: List[VariantForActiveTask]
    related_materials: List[ShortMaterialResponse]


class ShortLastHomework(PyBaseModel):
    id: UUID
    topic: str
    student_mark: int
    max_mark: int


class ShortLastHWTeacher(PyBaseModel):
    id: UUID
    topic: str


class LastHomework(ShortLastHomework):
    task_type_variants: List[VariantForLastTask]


class TeacherHomework(ActiveHomework):
    is_completed: bool
    task_type_variants: List[VariantForActiveTask]
    results: List[UserResultTask]


class CreateHomework(PyBaseModel):
    topic: str
    start_date: date
    end_date: date
    block_id: UUID
    class_id: UUID
    variants: List[VariantForCreateTask]


class EditHomework(PyBaseModel):
    topic: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
