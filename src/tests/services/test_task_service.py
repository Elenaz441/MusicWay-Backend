import pytest
from unittest.mock import patch
from uuid import uuid4
from services.task_service import TaskService
from schemas import TaskResponse, VariantForCreateTask, TaskSubmit, TaskAnswer
from exceptions import NotFoundException, NoRightsException


@pytest.fixture
def task_service(mock_task_repo, mock_variant_repo, mock_hw_task_repo, mock_task_type_repo):
    return TaskService(
        task_repo=mock_task_repo,
        variant_repo=mock_variant_repo,
        hw_task_repo=mock_hw_task_repo,
        task_type_repo=mock_task_type_repo
    )


@pytest.mark.asyncio
async def test_get_task_success(task_service):
    role = 'Ученик'
    task_info = {'id': uuid4(), 'variant_id': uuid4(), 'condition': 'Условие', 'content': {'a': 1}}
    task_service.variant_repo.find_one.return_value = {
        'name': 'Тип',
        'student_description': 'описание 1',
        'teacher_description': 'описание 2'
    }
    task_service.task_repo.find_one.return_value = task_info

    result = await task_service.get_task(role, id=task_info['id'])
    assert isinstance(result, TaskResponse)
    assert result.description == 'описание 1'


@pytest.mark.asyncio
async def test_get_task_success_teacher(task_service):
    role = 'Преподаватель'
    task_info = {'id': uuid4(), 'variant_id': uuid4(), 'condition': 'Условие', 'content': {'a': 1}}
    task_service.variant_repo.find_one.return_value = {
        'name': 'Тип', 'student_description': 'описание 1', 'teacher_description': 'описание 2'
    }
    task_service.task_repo.find_one.return_value = task_info

    result = await task_service.get_task(role, id=task_info['id'])
    assert result.description == 'описание 2'


@pytest.mark.asyncio
async def test_get_task_by_homework_success(task_service):
    homework_id = uuid4()
    task_id = uuid4()
    task_number = 1
    role = 'Ученик'

    task_service.hw_task_repo.find_all.return_value = [{'task_id': task_id}]
    task_service.task_repo.find_one.return_value = {
        'id': task_id,
        'variant_id': uuid4(),
        'condition': 'Условие',
        'content': {}
    }
    task_service.variant_repo.find_one.return_value = {'name': 'Тип', 'student_description': '', 'teacher_description': ''}

    result = await task_service.get_task_by_homework(role, homework_id, task_number)

    assert isinstance(result, TaskResponse)
    task_service.hw_task_repo.find_all.assert_awaited_once()
    task_service.task_repo.find_one.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_task_by_homework_no_rights(task_service):
    with pytest.raises(NoRightsException):
        await task_service.get_task_by_homework('Преподаватель', uuid4(), 1)


@pytest.mark.asyncio
async def test_get_task_not_found(task_service):
    task_service.task_repo.find_one.return_value = None
    with pytest.raises(NotFoundException):
        await task_service.get_task('Ученик', id=uuid4())


@pytest.mark.asyncio
async def test_check_task_not_found(task_service):
    task_service.task_repo.find_one.return_value = None
    with pytest.raises(NotFoundException):
        await task_service.check_task(uuid4(), TaskSubmit(check_data={}, delete_it=False))


@pytest.mark.asyncio
@patch('services.task_service.send_query')
async def test_create_task_success(mock_send_query, task_service):
    role = 'Ученик'
    variant_id = uuid4()
    data = VariantForCreateTask(variant_id=variant_id, settings={})

    task_service.variant_repo.find_one.return_value = {
        'task_type_id': uuid4(),
        'name': 'Тип',
        'student_description': 'описание',
        'teacher_description': 'описание'
    }
    task_service.task_type_repo.find_one.return_value = {'service_url': 'http://fake'}
    mock_send_query.return_value = [{
        'condition': 'Условие',
        'content': {'data': 1},
        'answer': {},
        'max_mark': 5
    }]
    task_service.task_repo.add_one.return_value = uuid4()
    task_service.task_repo.find_one.return_value = {'id': uuid4(), 'variant_id': variant_id, 'condition': 'Условие', 'content': {'data': 1}}

    result = await task_service.create_task(data, role)
    assert isinstance(result, TaskResponse)
    mock_send_query.assert_awaited_once()
    task_service.task_repo.add_one.assert_awaited_once()


@pytest.mark.asyncio
@patch('services.task_service.send_query')
async def test_check_task_success(mock_send_query, task_service):
    task_id = uuid4()
    data = TaskSubmit(check_data={'value': '42'}, delete_it=True)

    task_service.task_repo.find_one.return_value = {
        'id': task_id,
        'answer': {},
        'is_study_task': False,
        'variant_id': uuid4()
    }
    task_service.variant_repo.find_one.return_value = {'task_type_id': uuid4()}
    task_service.task_type_repo.find_one.return_value = {'service_url': 'http://fake'}
    mock_send_query.return_value = {'is_right': True, 'answer': {}}

    result = await task_service.check_task(task_id, data)
    assert isinstance(result, TaskAnswer)
    assert result.is_right is True
    task_service.task_repo.delete_one.assert_awaited_once_with(task_id)
