from .base import PyBaseModel
from .setting import IntervalsSettingResponse

from typing import Optional, Dict, Any


class CreateTaskSetting(IntervalsSettingResponse):
    count: Optional[int] = 1


class TaskResponse(PyBaseModel):
    condition: str
    content: Optional[Dict[str, Any]] = {}
    answer: Dict[str, Any]
    max_mark: int
    query: Optional[str] = None
