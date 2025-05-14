import pytest
import base64
from unittest.mock import patch

from services.task_service import TaskService
from schemas import (
    CreateTaskSetting,
    TaskResponse,
    CheckTask,
    CheckTaskResponse,
    GetMarkTaskResponse,
    CheckData,
    Answer
)


@pytest.fixture
def task_service(mock_audio_repo, mock_setting_repo):
    return TaskService(mock_audio_repo, mock_setting_repo)


@pytest.mark.asyncio
async def test_create_task_with_all_intervals(task_service):
    task_service.setting_repo.find_one.return_value = {'values': ['Все', 'б.2', 'ч.1']}
    task_service.audio_repo.find_random_audio.return_value = {
        'interval': 'б.2',
        'notes': ['До', 'Ре'],
        'url': 'http://audio.url/sample.mp3',
    }

    settings = CreateTaskSetting(count=2, intervals=['Все'])
    result = await task_service.create_task(settings)

    assert isinstance(result, list)
    assert len(result) == 2
    for task in result:
        assert isinstance(task, TaskResponse)
        assert 'Пропой восходящий интервал' in task.condition
        assert task.answer.note_1 == 'До'
        assert task.answer.note_2 == 'Ре'


@pytest.mark.asyncio
async def test_create_task_with_specific_intervals(task_service):
    task_service.audio_repo.find_random_audio.return_value = {
        'interval': 'ч.5',
        'notes': ['Соль', 'Ре'],
        'url': 'http://example.com/audio.mp3',
    }

    settings = CreateTaskSetting(count=1, intervals=['ч.5'])
    result = await task_service.create_task(settings)

    assert len(result) == 1
    task = result[0]
    assert task.query == 'ч.5'
    assert task.answer.note_1 == 'Соль'
    assert task.answer.note_2 == 'Ре'


@pytest.mark.asyncio
@patch('services.task_service.get_common_note', side_effect=['C4', 'E4'])
async def test_check_task_correct(get_note_mock, task_service):
    audio_1 = base64.b64encode(b'dummy1').decode()
    audio_2 = base64.b64encode(b'dummy2').decode()

    task = CheckTask(
        answer=Answer(note_1='До', note_2='Ми', audio_url='url'),
        check_data=CheckData(audio_1=audio_1, audio_2=audio_2),
    )

    result = await task_service.check_task(task)

    assert isinstance(result, CheckTaskResponse)
    assert result.is_right is True
    assert result.answer.audio_url == 'url'


@pytest.mark.asyncio
@patch('services.task_service.get_common_note', side_effect=['C4', 'F4'])
async def test_check_task_incorrect(get_note_mock, task_service):
    audio_1 = base64.b64encode(b'dummy1').decode()
    audio_2 = base64.b64encode(b'dummy2').decode()

    task = CheckTask(
        answer=Answer(note_1='До', note_2='Ми', audio_url='url'),
        check_data=CheckData(audio_1=audio_1, audio_2=audio_2),
    )

    result = await task_service.check_task(task)

    assert result.is_right is False


@pytest.mark.asyncio
@patch.object(TaskService, 'check_task', return_value=CheckTaskResponse(is_right=True, answer={'audio_url': 'url'}))
async def test_get_mark_right(mock_check, task_service):
    task = CheckTask(
        answer=Answer(note_1='До', note_2='Ми', audio_url='url'),
        check_data=CheckData(audio_1='audio_1', audio_2='audio_2')
    )
    result = await task_service.get_mark(task)

    assert isinstance(result, GetMarkTaskResponse)
    assert result.mark == 1


@pytest.mark.asyncio
@patch.object(TaskService, 'check_task', return_value=CheckTaskResponse(is_right=False, answer={'audio_url': 'url'}))
async def test_get_mark_wrong(mock_check, task_service):
    task = CheckTask(
        answer=Answer(note_1='До', note_2='Ми', audio_url='url'),
        check_data=CheckData(audio_1='...', audio_2='...')
    )
    result = await task_service.get_mark(task)

    assert result.mark == 0
