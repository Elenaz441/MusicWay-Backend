from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from repositories import VariantRepository


class Variant:
    id = MagicMock()
    name = MagicMock()
    student_description = MagicMock()


class TaskType:
    id = MagicMock()
    block_id = MagicMock()


@pytest.fixture
def mock_db_session():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def repo(mock_db_session):
    repo = VariantRepository(mock_db_session)
    return repo


@pytest.mark.asyncio
async def test_find_all_by_block(repo, mock_db_session):
    block_id = uuid4()
    test_fields = ['id', 'name', 'student_description']

    test_data = [
        {'id': uuid4(), 'name': 'Вариант 1', 'student_description': 'Описание 1'},
        {'id': uuid4(), 'name': 'Вариант 2', 'student_description': 'Описание 2'}
    ]

    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = test_data
    mock_db_session.execute.return_value = mock_result

    result = await repo.find_all_by_block(block_id, test_fields)

    mock_db_session.execute.assert_called_once()
    called_stmt = mock_db_session.execute.call_args[0][0]

    assert 'join task_type' in str(called_stmt).lower()
    assert 'task_type.block_id = :block_id' in str(called_stmt)

    assert len(result) == 2
    assert all(field in item for item in result for field in test_fields)


@pytest.mark.asyncio
async def test_find_all_by_block_minimal_fields(repo, mock_db_session):
    block_id = uuid4()
    test_fields = ['id', 'name']

    test_data = {'id': uuid4(), 'name': 'Минимальный вариант'}
    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = [test_data]
    mock_db_session.execute.return_value = mock_result

    result = await repo.find_all_by_block(block_id, test_fields)

    called_stmt = mock_db_session.execute.call_args[0][0]
    assert 'SELECT variant.id, variant.name' in str(called_stmt)

    assert len(result) == 1
    assert list(result[0].keys()) == test_fields


@pytest.mark.asyncio
async def test_find_all_by_block_empty_result(repo, mock_db_session):
    block_id = uuid4()
    test_fields = ['id', 'name']

    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = []
    mock_db_session.execute.return_value = mock_result

    result = await repo.find_all_by_block(block_id, test_fields)
    assert result == []


@pytest.mark.asyncio
async def test_find_all_by_block_with_ordering(repo, mock_db_session):
    block_id = uuid4()
    test_fields = ['id', 'name']

    test_data = [
        {'id': uuid4(), 'name': 'Вариант A'},
        {'id': uuid4(), 'name': 'Вариант B'}
    ]
    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = test_data
    mock_db_session.execute.return_value = mock_result

    result = await repo.find_all_by_block(block_id, test_fields)

    assert len(result) == 2
    assert result[0]['name'] == 'Вариант A'
    assert result[1]['name'] == 'Вариант B'
