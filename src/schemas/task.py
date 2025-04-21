from .base import PyBaseModel

from typing import List, Optional
from uuid import UUID


class CreateTaskSetting(PyBaseModel):
    melodies: Optional[List[UUID]] = None


class AnswerResponse(PyBaseModel):
    audio_url: str
    image_url: str


class Answer(PyBaseModel):
    melody: UUID


class Content(PyBaseModel):
    initial_note: str
    intervals: List[str]


class TaskResponse(PyBaseModel):
    condition: str
    content: Content
    answer: Answer
    max_mark: int
    query: str


class CheckData(PyBaseModel):
    notes: List[str]


class CheckTask(PyBaseModel):
    check_data: CheckData
    answer: Answer


class CheckTaskResponse(PyBaseModel):
    is_right: bool
    answer: AnswerResponse


class GetMarkTaskResponse(PyBaseModel):
    mark: int
