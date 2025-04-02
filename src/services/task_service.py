import random
import base64

from repositories import AudioRepo, SettingRepo
from schemas import CreateTaskSetting, TaskResponse, CheckTask, CheckTaskResponse, GetMarkTaskResponse
from utils import get_common_note, convert_russian_note_to_international

from typing import List


class TaskService:
    """Сервис для работы с заданиями."""

    def __init__(self, audio_repo: AudioRepo, setting_repo: SettingRepo):
        self.audio_repo = audio_repo
        self.setting_repo = setting_repo

    async def create_task(self, settings: CreateTaskSetting) -> List[TaskResponse]:
        """Создает упражнение по переданным настройкам"""
        tasks = []
        intervals = settings.intervals
        if 'Все' in intervals:
            intervals = await self.setting_repo.find_one(['values'], name='Интервалы')
            intervals = dict(intervals)['values'][1:]
        for i in range(settings.count):
            task = {}
            interval = intervals[i % len(intervals)]
            audio = await self.audio_repo.find_random_audio(['interval', 'notes', 'url'], interval=interval)
            task['condition'] = f'Пропой восходящий интервал {audio.interval} от ноты {audio.notes[0]}'
            task['answer'] = {
                'audio_url': audio.url,
                'note_1': audio.notes[0],
                'note_2': audio.notes[1],
            }
            task['max_mark'] = 1
            task['query'] = interval
            tasks.append(TaskResponse.model_validate(task))
        random.shuffle(tasks)
        return tasks

    async def check_task(self, task: CheckTask) -> CheckTaskResponse:
        """Проверяет правильность выполнения упражнения"""
        audio_1 = base64.b64decode(task.check_data.audio_1)
        user_note_1 = get_common_note(audio_1)
        answer_note_1 = convert_russian_note_to_international(task.answer.note_1)
        audio_2 = base64.b64decode(task.check_data.audio_2)
        user_note_2 = get_common_note(audio_2)
        answer_note_2 = convert_russian_note_to_international(task.answer.note_2)
        return CheckTaskResponse(
            is_right=user_note_1 == answer_note_1 and user_note_2 == answer_note_2,
            answer={'audio_url': task.answer.audio_url}
        )

    async def get_mark(self, task: CheckTask) -> GetMarkTaskResponse:
        """Выставляет балл за упражнение"""
        check = await self.check_task(task)
        return GetMarkTaskResponse(mark=int(check.is_right))

