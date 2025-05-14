import random

from repositories import MelodyRepo
from schemas import CreateTaskSetting, TaskResponse, CheckTask, CheckTaskResponse, GetMarkTaskResponse
from exceptions import NotFoundException
from utils import convert_russian_note_to_international, calculate_interval

from typing import List


class TaskService:
    """Сервис для работы с заданиями."""

    def __init__(self, melody_repo: MelodyRepo):
        self.melody_repo = melody_repo

    async def create_task(self, settings: CreateTaskSetting) -> List[TaskResponse]:
        """Создает упражнение по переданным настройкам.

        :param settings: Настройки для создания.

        :return: Список упражнений.
        """
        melodies = settings.melodies
        if settings.melodies is None:
            melody = await self.melody_repo.find_random_melody(['id'])
            melodies = [melody['id']]
        tasks = []
        for melody_id in melodies:
            task = {}
            melody = await self.melody_repo.find_one(
                ['name', 'notes', 'intervals', 'audio_url', 'image_url', 'query'],
                id=melody_id
            )
            if not melody:
                raise NotFoundException('мелодия', 'id')
            task['condition'] = f'Построй интервал {melody["intervals"][0]} от ноты {melody["notes"][0]}'
            task['content'] = {
                'initial_note': convert_russian_note_to_international(melody['notes'][0]),
                'intervals': [f'Построй интервал {interval}' for interval in melody['intervals'][1:]]
            }
            task['answer'] = {
                'audio_url': melody['audio_url'],
                'image_url': melody['image_url'],
                'melody': melody_id,
            }
            task['max_mark'] = 10
            task['query'] = melody['query']
            tasks.append(TaskResponse.model_validate(task))
        random.shuffle(tasks)
        return tasks

    async def check_task(self, task: CheckTask) -> CheckTaskResponse:
        """Проверяет правильность выполнения упражнения.

        :param task: Упражнение для проверки.

        :return: Результат проверки.
        """
        is_right = True
        melody = await self.melody_repo.find_one(['notes', 'audio_url', 'image_url'], id=task.answer.melody)
        if not melody:
            raise NotFoundException('мелодия', 'id')
        for i in range(len(task.check_data.notes)):
            right_note = convert_russian_note_to_international(melody['notes'][i])
            if right_note != task.check_data.notes[i]:
                is_right = False
                break
        return CheckTaskResponse(
            is_right=is_right,
            answer={'audio_url': melody['audio_url'], 'image_url': melody['image_url']}
        )

    async def get_mark(self, task: CheckTask) -> GetMarkTaskResponse:
        """Выставляет балл за упражнение

        :param task: Упражнение для выставления баллов.

        :return: Балл за упражнение.
        """
        mark = 10
        check = await self.check_task(task)
        if check.is_right:
            return GetMarkTaskResponse(mark=mark)
        melody = await self.melody_repo.find_one(['intervals'], id=task.answer.melody)
        intervals = [
            calculate_interval(task.check_data.notes[i - 1], task.check_data.notes[i])
            for i in range(1, len(task.check_data.notes))
        ]
        mistakes = -1
        for i in range(len(intervals)):
            if intervals[i] != melody['intervals'][i]:
                mistakes += 1
        if mistakes == -1:
            mistakes = 0
        if mistakes >= 11:
            mistakes = mark = 0
        return GetMarkTaskResponse(mark=mark - mistakes)
