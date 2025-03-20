from .base import PyBaseModel
from .task import TaskResultForTeacher
from .topic_block import TopicBlockResponse

from typing import List, Optional
from uuid import UUID


class UserResultTask(PyBaseModel):
    name: str
    surname: str
    patronymic: Optional[str] = None
    student_mark: Optional[int] = None
    tasks: List[TaskResultForTeacher]


class UserInfo(PyBaseModel):
    id: UUID
    name: str
    surname: str
    patronymic: Optional[str] = None


class UserStatistic(PyBaseModel):
    success_rate: int
    topic_blocks: List[TopicBlockResponse]
