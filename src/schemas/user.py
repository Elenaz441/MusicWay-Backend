from .base import PyBaseModel
from .task import TaskResultForTeacher

from typing import List, Optional


class UserResultTask(PyBaseModel):
    name: str
    surname: str
    patronymic: Optional[str] = None
    student_mark: Optional[int] = None
    tasks: List[TaskResultForTeacher]
