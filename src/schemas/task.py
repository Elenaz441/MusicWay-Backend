from .base import PyBaseModel
from uuid import UUID
from typing import Dict, Any, Optional


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


class TaskResultForTeacher(PyBaseModel):
    name: str
    student_mark: Optional[int]
    max_mark: int


class TaskSubmit(PyBaseModel):
    check_data: Dict[str, Any]


class TaskHomeworkSubmit(TaskSubmit):
    task_id: UUID
