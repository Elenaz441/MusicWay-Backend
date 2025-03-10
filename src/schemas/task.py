from .base import PyBaseModel
from uuid import UUID
from typing import Dict, Any


class TaskResponse(PyBaseModel):
    id: UUID
    condition: str
    task_type_variant: str
    description: str
    content: Dict[str, Any]


class TaskForLastHomework(PyBaseModel):
    number: int
    student_mark: int
    max_mark: int
