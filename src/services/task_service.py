import random

from repositories import AudioRepo, SettingRepo
from schemas import CreateTaskSetting, TaskResponse
from random import randint

from typing import List


class TaskService:
    """Сервис для работы с заданиями."""

    def __init__(self, audio_repo: AudioRepo, setting_repo: SettingRepo):
        self.audio_repo = audio_repo
        self.setting_repo = setting_repo

    async def create_task(self, settings: CreateTaskSetting) -> List[TaskResponse]:
        """Создает задание по переданным настройкам"""
        tasks = []
        intervals = settings.intervals
        if 'Все' in intervals:
            intervals = await self.setting_repo.find_one(['values'], name='Интервалы')
            intervals = dict(intervals)['values'][1:]
        for i in range(settings.count):
            task = {}
            interval = intervals[i % len(intervals)]
            audio = await self.audio_repo.get_random_audio(['interval', 'notes', 'url'], interval=interval)
            task['condition'] = f'Пропой восходящий интервал {audio.interval} от ноты {audio.notes[0]}'
            task['answer'] = {
                'audio_url': audio.url,
            }
            task['max_mark'] = 1
            task['query'] = interval
            tasks.append(TaskResponse.model_validate(task))
        random.shuffle(tasks)
        return tasks
