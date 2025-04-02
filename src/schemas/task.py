from .base import PyBaseModel
from .setting import IntervalsSettingResponse

from typing import Optional, Dict, Any


class CreateTaskSetting(IntervalsSettingResponse):
    count: Optional[int] = 1


class AnswerResponse(PyBaseModel):
    audio_url: str


class Answer(AnswerResponse):
    note_1: str
    note_2: str


class TaskResponse(PyBaseModel):
    condition: str
    content: Optional[Dict[str, Any]] = {}
    answer: Answer
    max_mark: int
    query: Optional[str] = None


class CheckData(PyBaseModel):
    audio_1: str
    audio_2: str


class CheckTask(PyBaseModel):
    check_data: CheckData
    answer: Answer


class CheckTaskResponse(PyBaseModel):
    is_right: bool
    answer: AnswerResponse


class GetMarkTaskResponse(PyBaseModel):
    mark: int
