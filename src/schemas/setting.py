from .base import PyBaseModel
from typing import List


class IntervalsSettingResponse(PyBaseModel):
    intervals: List[str]

