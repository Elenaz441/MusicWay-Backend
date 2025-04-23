import random

from repositories import AudioRepo, SettingRepo, ImageRepo
from schemas import CreateTaskSetting, TaskResponse, CheckTask, CheckTaskResponse, GetMarkTaskResponse, MarkRequest

from typing import List


class TaskService:
    """Сервис для работы с заданиями."""

    def __init__(self, image_repo: ImageRepo, audio_repo: AudioRepo, setting_repo: SettingRepo):
        self.image_repo = image_repo
        self.audio_repo = audio_repo
        self.setting_repo = setting_repo

    async def create_task(self, settings: CreateTaskSetting) -> List[TaskResponse]:
        """Создает упражнение по переданным настройкам.

        :param settings: Настройки для создания.

        :return: Список упражнений.
        """
        tasks = []
        intervals = settings.intervals
        if 'Все' in intervals:
            intervals = await self.setting_repo.find_one(['values'], name='Интервалы')
            intervals = dict(intervals)['values'][1:]
        images = await self.image_repo.find_random_image(['name', 'url'], settings.count)
        for i in range(settings.count):
            task = {}
            query = intervals[i % len(intervals)]

            selected = []
            selected.extend(random.sample(intervals, min(len(intervals), 4)))
            while len(selected) < 4:
                selected.append(random.choice(intervals))

            audios = []
            answer = []
            for interval in selected:
                audio = await self.audio_repo.find_random_audio(['interval', 'url'], interval=interval)
                audios.append(audio.url)
                answer.append({'audio_url': audio.url, 'interval': interval})
            random.shuffle(selected)
            task['content'] = {
                'image_url': images[i % len(images)].url,
                'image_name': images[i % len(images)].name,
                'audio_urls': audios,
                'intervals': selected
            }
            task['condition'] = ''
            task['answer'] = answer
            task['max_mark'] = 6
            task['query'] = query
            tasks.append(TaskResponse.model_validate(task))
        return tasks

    async def check_task(self, task: CheckTask) -> CheckTaskResponse:
        """Проверяет правильность выполнения упражнения.

        :param task: Упражнение для проверки.

        :return: Результат проверки.
        """
        return CheckTaskResponse(
            is_right=task.check_data.interval == task.answer[task.check_data.audio_number].interval,
            answer=None
        )

    async def get_mark(self, task: MarkRequest) -> GetMarkTaskResponse:
        """Выставляет балл за упражнение

        :param task: Упражнение для выставления баллов.

        :return: Балл за упражнение.
        """
        mistakes_count = task.check_data.mistakes_count
        mistakes = 6 if mistakes_count > 6 else mistakes_count
        return GetMarkTaskResponse(mark=6 - mistakes)
