import pytest
from unittest.mock import patch

from services.task_service import TaskService
from schemas import (
    CreateTaskSetting,
    TaskResponse,
    CheckTask,
    CheckTaskResponse,
    GetMarkTaskResponse,
    CheckData,
    Answer,
    MarkRequest
)


@pytest.fixture
def task_service(mock_image_repo, mock_audio_repo, mock_setting_repo):
    return TaskService(mock_image_repo, mock_audio_repo, mock_setting_repo)


@pytest.mark.asyncio
@patch('random.sample', side_effect=lambda x, k: x[:k])
@patch('random.choice', side_effect=lambda x: x[0])
async def test_create_task_with_all_intervals(mock_choice, mock_sample, task_service):
    task_service.setting_repo.find_one.return_value = {'values': ['Все', 'м.3', 'ч.1']}
    task_service.image_repo.find_random_image.return_value = [
        {'url': 'http://image.url/1.png', 'name': 'Image 1'},
        {'url': 'http://image.url/2.png', 'name': 'Image 2'},
    ]
    task_service.audio_repo.find_random_audio.return_value = {
        'url': 'http://audio.url/sample.mp3',
        'interval': 'м.3'
    }

    settings = CreateTaskSetting(count=2, intervals=['Все'])
    tasks = await task_service.create_task(settings)

    assert len(tasks) == 2
    for task in tasks:
        assert isinstance(task, TaskResponse)
        assert len(task.content.audio_urls) == 4
        assert len(task.content.intervals) == 4
        assert task.max_mark == 6


@pytest.mark.asyncio
async def test_check_task_correct(task_service):
    task = CheckTask(
        answer=[
            Answer(audio_url='a1', interval='м.3'),
            Answer(audio_url='a2', interval='ч.1')
        ],
        check_data=CheckData(interval='ч.1', audio_number=1)
    )
    result = await task_service.check_task(task)

    assert isinstance(result, CheckTaskResponse)
    assert result.is_right is True


@pytest.mark.asyncio
async def test_check_task_incorrect(task_service):
    task = CheckTask(
        answer=[
            Answer(audio_url='a1', interval='м.3'),
            Answer(audio_url='a2', interval='ч.1')
        ],
        check_data=CheckData(interval='ч.4', audio_number=1)
    )
    result = await task_service.check_task(task)

    assert isinstance(result, CheckTaskResponse)
    assert result.is_right is False


@pytest.mark.asyncio
@pytest.mark.parametrize('mistakes_count, expected_mark', [
    (0, 6),
    (2, 4),
    (6, 0),
    (8, 0),
])
async def test_get_mark(task_service, mistakes_count, expected_mark):
    task = MarkRequest(
        check_data={'mistakes_count': mistakes_count},
        answer=[
            Answer(audio_url='a1', interval='м.3'),
            Answer(audio_url='a2', interval='ч.1')
        ]
    )
    result = await task_service.get_mark(task)

    assert isinstance(result, GetMarkTaskResponse)
    assert result.mark == expected_mark
