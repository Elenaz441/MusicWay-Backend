from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from repositories import MaterialRepository


class StudyMaterial:
    id = MagicMock()
    name = MagicMock()
    number = MagicMock()
    block_id = MagicMock()
    search_vector = MagicMock()


class Task:
    material_id = MagicMock()


class HomeworkTask:
    task_id = MagicMock()
    homework_id = MagicMock()


@pytest.fixture
def mock_db_session():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def repo(mock_db_session):
    repo = MaterialRepository(mock_db_session)
    return repo


@pytest.mark.asyncio
async def test_find_all_with_search(repo, mock_db_session):
    test_fields = ['id', 'name']
    test_filter = {'search_vector': 'поисковый запрос'}

    test_data = [
        {'id': uuid4(), 'name': 'Материал 1'},
        {'id': uuid4(), 'name': 'Материал 2'},
    ]

    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = test_data
    mock_db_session.execute.return_value = mock_result

    result = await repo.find_all(test_fields, test_filter)

    mock_db_session.execute.assert_called_once()
    called_stmt = mock_db_session.execute.call_args[0][0]

    assert 'search_vector @@ plainto_tsquery' in str(called_stmt)

    assert len(result) == 2
    assert all('id' in item and 'name' in item for item in result)


@pytest.mark.asyncio
async def test_find_all_with_regular_filter(repo, mock_db_session):
    test_fields = ['id', 'block_id']
    test_filter = {'block_id': uuid4()}

    test_data = [{'id': uuid4(), 'block_id': test_filter['block_id']}]
    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = test_data
    mock_db_session.execute.return_value = mock_result

    result = await repo.find_all(test_fields, test_filter)

    called_stmt = mock_db_session.execute.call_args[0][0]
    assert 'study_material.block_id = :block_id' in str(called_stmt)
    assert result[0]['block_id'] == test_filter['block_id']


@pytest.mark.asyncio
async def test_find_all_by_homework(repo, mock_db_session):
    homework_id = uuid4()

    expected_fields = {
        'id': uuid4(),
        'name': 'Тестовый материал',
        'number': 1,
        'block_id': uuid4()
    }

    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = [expected_fields]
    mock_db_session.execute.return_value = mock_result

    result = await repo.find_all_by_homework(homework_id)

    mock_db_session.execute.assert_called_once()
    called_stmt = mock_db_session.execute.call_args[0][0]

    assert 'join task on task.material_id = study_material.id' in str(called_stmt).lower()
    assert 'join homework_task on homework_task.task_id = task.id' in str(called_stmt).lower()

    assert 'homework_task.homework_id = :homework_id' in str(called_stmt).lower()

    assert 'order by study_material.block_id, study_material.number' in str(called_stmt).lower()

    assert 'DISTINCT' in str(called_stmt).upper()

    assert len(result) == 1
    assert result[0] == expected_fields


@pytest.mark.asyncio
async def test_find_all_empty_result(repo, mock_db_session):
    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = []
    mock_db_session.execute.return_value = mock_result

    result = await repo.find_all(['id', 'name'])
    assert result == []


@pytest.mark.asyncio
async def test_find_all_ordering_and_limit(repo, mock_db_session):
    test_fields = ['id', 'name']
    test_order = 'name'
    test_limit = 5

    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = [{'id': uuid4(), 'name': f'Material {i}'} for i in range(3)]
    mock_db_session.execute.return_value = mock_result

    result = await repo.find_all(
        test_fields,
        order_by=test_order,
        limit=test_limit
    )

    called_stmt = mock_db_session.execute.call_args[0][0]
    assert 'ORDER BY study_material.name' in str(called_stmt)
    assert 'LIMIT' in str(called_stmt)
    assert len(result) == 3
