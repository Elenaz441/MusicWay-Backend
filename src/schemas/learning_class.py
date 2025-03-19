from .base import PyBaseModel
from .user import UserInfo
from .homework import ShortActiveHomework
from datetime import time
from uuid import UUID
from typing import List


class ShortClassResponse(PyBaseModel):
    id: UUID
    class_number: int
    week_day: str
    class_time: time


class ClassResponse(ShortClassResponse):
    students: List[UserInfo]
    active_homeworks: List[ShortActiveHomework]
