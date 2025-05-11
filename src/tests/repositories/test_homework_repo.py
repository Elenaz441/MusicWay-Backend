from uuid import uuid4
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from repositories import HomeworkRepository


class Homework:
    id = MagicMock()
    topic = MagicMock()
    start_date = MagicMock()
    end_date = MagicMock()
    block_id = MagicMock()
    class_id = MagicMock()


class HomeworkTask:
    id = MagicMock()
    homework_id = MagicMock()
    task_id = MagicMock()
    student_id = MagicMock()
    mark = MagicMock()


class Task:
    id = MagicMock()
    max_mark = MagicMock()
    variant_id = MagicMock()
    number = MagicMock()


class TopicBlock:
    id = MagicMock()
    name = MagicMock()


class User:
    id = MagicMock()
    name = MagicMock()
    surname = MagicMock()
    patronymic = MagicMock()


class Variant:
    id = MagicMock()
    name = MagicMock()


@pytest.fixture
def mock_db_session():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def repo(mock_db_session):
    repo = HomeworkRepository(mock_db_session)
    return repo


@pytest.mark.asyncio
async def test_find_one_with_mark(repo, mock_db_session):
    homework_id = uuid4()
    student_id = uuid4()
    test_data = {
        'id': homework_id,
        'topic': 'Test Topic',
        'start_date': datetime.now(),
        'end_date': datetime.now() + timedelta(days=7),
        'block': 'Test Block',
        'student_mark': 85,
        'max_mark': 100,
        'count': 5
    }

    mock_result = MagicMock()
    mock_result.mappings.return_value.first.return_value = test_data
    mock_db_session.execute.return_value = mock_result

    result = await repo.find_one_with_mark(homework_id, student_id)

    mock_db_session.execute.assert_called_once()
    assert result == test_data


@pytest.mark.asyncio
async def test_find_all_active(repo, mock_db_session):
    class_id = uuid4()
    test_data = [
        {'id': uuid4(), 'topic': 'Topic 1', 'max_mark': 100, 'count': 5},
        {'id': uuid4(), 'topic': 'Topic 2', 'max_mark': 150, 'count': 7}
    ]

    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = test_data
    mock_db_session.execute.return_value = mock_result

    result = await repo.find_all_active(class_id)
    assert len(result) == 2
    assert result == test_data

    student_id = uuid4()
    await repo.find_all_active(class_id, student_id)
    mock_db_session.execute.assert_called()


@pytest.mark.asyncio
async def test_find_all_completed(repo, mock_db_session):
    filter_by = {'class_id': uuid4(), 'student_id': uuid4()}
    test_data = [
        {'id': uuid4(), 'topic': 'Completed 1', 'student_mark': 90, 'max_mark': 100},
        {'id': uuid4(), 'topic': 'Completed 2', 'student_mark': 75, 'max_mark': 100}
    ]

    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = test_data
    mock_db_session.execute.return_value = mock_result

    result = await repo.find_all_completed(filter_by)
    assert len(result) == 2
    assert all('student_mark' in item for item in result)


# @pytest.mark.asyncio
# async def test_is_completed(repo, mock_db_session):
#     homework_id = uuid4()
#     student_id = uuid4()
#
#     mock_db_session.execute.return_value.scalar.return_value = True
#     assert await repo.is_completed(homework_id, student_id) is True
#
#     mock_db_session.execute.return_value.scalar.return_value = False
#     assert await repo.is_completed(homework_id, student_id) is False

@pytest.mark.asyncio
async def test_is_completed(repo, mock_db_session):
    homework_id = uuid4()
    student_id = uuid4()

    mock_result = MagicMock()

    mock_result.scalar.return_value = True
    mock_db_session.execute.return_value = mock_result

    result = await repo.is_completed(homework_id, student_id)
    assert result is True

    mock_result.scalar.return_value = False
    result = await repo.is_completed(homework_id, student_id)
    assert result is False


@pytest.mark.asyncio
async def test_get_marks(repo, mock_db_session):
    homework_id = uuid4()
    test_data = [
        {'name': 'Variant 1', 'number': 1, 'student_mark': 5, 'max_mark': 10},
        {'name': 'Variant 2', 'number': 2, 'student_mark': 8, 'max_mark': 10}
    ]

    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = test_data
    mock_db_session.execute.return_value = mock_result

    result = await repo.get_marks(homework_id)
    assert len(result) == 2
    assert all('student_mark' in item for item in result)

    student_id = uuid4()
    await repo.get_marks(homework_id, student_id)
    mock_db_session.execute.assert_called()


@pytest.mark.asyncio
async def test_get_homework_students(repo, mock_db_session):
    homework_id = uuid4()
    test_data = [
        {'id': uuid4(), 'name': 'John', 'surname': 'Doe', 'student_mark': 85},
        {'id': uuid4(), 'name': 'Jane', 'surname': 'Smith', 'student_mark': 92}
    ]

    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = test_data
    mock_db_session.execute.return_value = mock_result

    result = await repo.get_homework_students(homework_id)
    assert len(result) == 2
    assert all('student_mark' in item for item in result)


@pytest.mark.asyncio
async def test_get_homework_tasks(repo, mock_db_session):
    homework_id = uuid4()
    test_data = [
        {'student_id': uuid4(), 'task_name': 'Task 1', 'student_mark': 5, 'max_mark': 10},
        {'student_id': uuid4(), 'task_name': 'Task 2', 'student_mark': 8, 'max_mark': 10}
    ]

    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = test_data
    mock_db_session.execute.return_value = mock_result

    result = await repo.get_homework_tasks(homework_id)
    assert len(result) == 2
    assert all('max_mark' in item for item in result)


@pytest.mark.asyncio
async def test_get_statistic(repo, mock_db_session):
    class_id = uuid4()
    test_data = [
        {'id': uuid4(), 'topic': 'Topic 1', 'success_rate': 85},
        {'id': uuid4(), 'topic': 'Topic 2', 'success_rate': 72}
    ]

    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = test_data
    mock_db_session.execute.return_value = mock_result

    result = await repo.get_statistic(class_id)
    assert len(result) == 2
    assert all('success_rate' in item for item in result)
