from .base import PyBaseModel

from typing import Optional, List


class CreateTaskSetting(PyBaseModel):
    intervals: List[str]
    count: Optional[int] = 1


class AnswerResponse(PyBaseModel):
    pass


class Answer(AnswerResponse):
    audio_url: str
    interval: str


class Content(PyBaseModel):
    image_url: str
    image_name: str
    audio_urls: List[str]
    intervals: List[str]


class TaskResponse(PyBaseModel):
    condition: str
    content: Content
    answer: List[Answer]
    max_mark: int
    query: Optional[str] = None


class CheckData(PyBaseModel):
    audio_number: int
    interval: str


class CheckTask(PyBaseModel):
    check_data: CheckData
    answer: List[Answer]


class CheckTaskResponse(PyBaseModel):
    is_right: bool
    answer: Optional[AnswerResponse] = None


class MistakesCount(PyBaseModel):
    mistakes_count: int


class MarkRequest(PyBaseModel):
    check_data: MistakesCount
    answer: List[Answer]


class GetMarkTaskResponse(PyBaseModel):
    mark: int
