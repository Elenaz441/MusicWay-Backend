import pytest
from uuid import uuid4
from services.task_service import TaskService
from schemas import (
    CreateTaskSetting,
    CheckTask,
    CheckTaskResponse,
    GetMarkTaskResponse,
    TaskResponse
)
from exceptions import NotFoundException


@pytest.fixture
def task_service(mock_melody_repo):
    return TaskService(melody_repo=mock_melody_repo)


@pytest.mark.asyncio
async def test_create_task_with_given_melodies(task_service):
    melody_id = uuid4()
    task_service.melody_repo.find_one.return_value = {
        'name': 'Test Melody',
        'notes': ['до', 'ре', 'ми'],
        'intervals': ['м2', 'м2'],
        'audio_url': 'http://audio',
        'image_url': 'http://image',
        'query': 'query',
    }

    settings = CreateTaskSetting(melodies=[melody_id])
    result = await task_service.create_task(settings)

    assert len(result) == 1
    task = result[0]
    assert isinstance(task, TaskResponse)
    assert task.answer.melody == melody_id
    task_service.melody_repo.find_one.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_task_with_random_melody(task_service):
    melody_id = uuid4()
    task_service.melody_repo.find_random_melody.return_value = {'id': melody_id}
    task_service.melody_repo.find_one.return_value = {
        'name': 'Random Melody',
        'notes': ['до', 'ре'],
        'intervals': ['м2'],
        'audio_url': 'http://audio',
        'image_url': 'http://image',
        'query': 'query',
    }

    settings = CreateTaskSetting(melodies=None)
    result = await task_service.create_task(settings)

    assert len(result) == 1
    assert result[0].answer.melody == melody_id


@pytest.mark.asyncio
async def test_create_task_melody_not_found(task_service):
    task_service.melody_repo.find_one.return_value = None
    settings = CreateTaskSetting(melodies=[uuid4()])

    with pytest.raises(NotFoundException):
        await task_service.create_task(settings)


@pytest.mark.asyncio
async def test_check_task_correct_answer(task_service):
    task_service.melody_repo.find_one.return_value = {
        'notes': ['до', 'ре', 'ми'],
        'audio_url': 'http://audio',
        'image_url': 'http://image'
    }

    task = CheckTask(
        check_data={'notes': ['C4', 'D4', 'E4']},
        answer={'melody': uuid4()}
    )

    result = await task_service.check_task(task)

    assert isinstance(result, CheckTaskResponse)
    assert result.is_right is True


@pytest.mark.asyncio
async def test_check_task_incorrect_answer(task_service):
    task_service.melody_repo.find_one.return_value = {
        'notes': ['до', 'ре'],
        'audio_url': 'http://audio',
        'image_url': 'http://image'
    }

    task = CheckTask(
        check_data={'notes': ['C4', 'E4']},
        answer={'melody': uuid4()}
    )

    result = await task_service.check_task(task)

    assert result.is_right is False


@pytest.mark.asyncio
async def test_get_mark_full_points(task_service):
    task_service.melody_repo.find_one.return_value = {
        'notes': ['до', 'ре'],
        'audio_url': 'http://audio',
        'image_url': 'http://image'
    }

    task = CheckTask(
        check_data={'notes': ['C4', 'D4']},
        answer={'melody': uuid4()}
    )

    result = await task_service.get_mark(task)

    assert result.mark == 10


@pytest.mark.asyncio
async def test_get_mark_with_mistakes(task_service):
    task_service.melody_repo.find_one.return_value = {
        'notes': ['до', 'ре', 'ми'],
        'audio_url': 'http://audio',
        'intervals': ['б.2', 'б.2'],
        'image_url': 'http://image'
    }

    task = CheckTask(
        check_data={'notes': ['C4', 'F4', 'E4']},
        answer={'melody': uuid4()}
    )

    result = await task_service.get_mark(task)

    assert isinstance(result, GetMarkTaskResponse)
    assert result.mark == 9
