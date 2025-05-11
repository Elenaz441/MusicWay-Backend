from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from repositories import TaskRepository


class Task:
    id = MagicMock()
    variant_id = MagicMock()
    material_id = MagicMock()
    is_study_task = MagicMock()


class Variant:
    id = MagicMock()
    name = MagicMock()


class HomeworkTask:
    id = MagicMock()
    homework_id = MagicMock()
    task_id = MagicMock()
    student_id = MagicMock()


@pytest.fixture
def mock_db_session():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def repo(mock_db_session):
    repo = TaskRepository(mock_db_session)
    return repo


@pytest.mark.asyncio
async def test_find_one_with_task_ids(repo, mock_db_session):
    test_fields = ['id']
    test_task_ids = [uuid4(), uuid4()]
    test_filter = {'task_ids': test_task_ids}
    test_data = {'id': test_task_ids[0]}

    mock_result = MagicMock()
    mock_result.mappings.return_value.first.return_value = test_data
    mock_db_session.execute.return_value = mock_result

    result = await repo.find_one(test_fields, test_filter)

    mock_db_session.execute.assert_called_once()
    called_stmt = mock_db_session.execute.call_args[0][0]
    assert 'task.id in' in str(called_stmt).lower()
    assert result == test_data


@pytest.mark.asyncio
async def test_find_one_with_regular_filter(repo, mock_db_session):
    test_fields = ['id', 'variant_id']
    test_filter = {'variant_id': uuid4()}
    test_data = {'id': uuid4(), 'variant_id': test_filter['variant_id']}

    mock_result = MagicMock()
    mock_result.mappings.return_value.first.return_value = test_data
    mock_db_session.execute.return_value = mock_result

    result = await repo.find_one(test_fields, test_filter)
    assert result == test_data


@pytest.mark.asyncio
async def test_find_all_by_material(repo, mock_db_session):
    material_id = uuid4()
    test_data = [
        {'variant_id': uuid4(), 'name': 'Variant 1', 'count': 5},
        {'variant_id': uuid4(), 'name': 'Variant 2', 'count': 3}
    ]

    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = test_data
    mock_db_session.execute.return_value = mock_result

    result = await repo.find_all_by_material(material_id)

    called_stmt = mock_db_session.execute.call_args[0][0]
    assert 'join variant' in str(called_stmt).lower()
    assert 'group by' in str(called_stmt).lower()
    assert len(result) == 2
    assert all('count' in item for item in result)


@pytest.mark.asyncio
async def test_find_all_by_homework(repo, mock_db_session):
    homework_id = uuid4()
    student_id = uuid4()
    test_data = [
        {'variant_id': uuid4(), 'name': 'Variant A', 'count': 4},
        {'variant_id': uuid4(), 'name': 'Variant B', 'count': 6}
    ]

    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = test_data
    mock_db_session.execute.return_value = mock_result

    result = await repo.find_all_by_homework(homework_id, student_id)

    called_stmt = mock_db_session.execute.call_args[0][0]
    print(mock_db_session.execute.call_args[0][0])
    print(mock_db_session.execute.call_args[1])
    print(homework_id, student_id)
    assert 'join homework_task' in str(called_stmt).lower()
    assert len(result) == 2
    assert all(item['count'] > 0 for item in result)


@pytest.mark.asyncio
async def test_find_one_not_found(repo, mock_db_session):
    mock_result = MagicMock()
    mock_result.mappings.return_value.first.return_value = None
    mock_db_session.execute.return_value = mock_result

    result = await repo.find_one(['id'], {'variant_id': uuid4()})
    assert result is None


@pytest.mark.asyncio
async def test_find_all_empty_result(repo, mock_db_session):
    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = []
    mock_db_session.execute.return_value = mock_result

    result = await repo.find_all_by_material(uuid4())
    assert result == []

    result = await repo.find_all_by_homework(uuid4(), uuid4())
    assert result == []
