from .base import PyBaseModel
from typing import List


class IntervalsSettingResponse(PyBaseModel):
    description: str
    intervals: List[str]
    is_need_count: bool

