from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock
import pytest
from sqlalchemy import Column, String, Integer, UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from repositories import SQLAlchemyRepository

Base = declarative_base()


class MyTestModel(Base):
    __tablename__ = 'test_model'

    id = Column(UUID, primary_key=True, default=uuid4)
    name = Column(String)
    value = Column(Integer)


@pytest.fixture
def mock_db_session():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def repo(mock_db_session):
    repo = SQLAlchemyRepository(mock_db_session)
    repo.model = MyTestModel
    return repo


@pytest.mark.asyncio
async def test_add_one(repo, mock_db_session):
    test_data = {'name': 'test', 'value': 123}
    test_uuid = uuid4()

    mock_result = MagicMock()
    mock_result.scalar_one.return_value = test_uuid
    mock_db_session.execute.return_value = mock_result

    result = await repo.add_one(test_data)

    mock_db_session.execute.assert_called_once()
    mock_db_session.commit.assert_awaited_once()

    assert result == test_uuid


@pytest.mark.asyncio
async def test_edit_one(repo, mock_db_session):
    test_id = uuid4()
    test_data = {'name': 'updated', 'value': 456}

    mock_result = MagicMock()
    mock_result.scalar_one.return_value = test_id
    mock_db_session.execute.return_value = mock_result

    result = await repo.edit_one(test_id, test_data)

    mock_db_session.execute.assert_called_once()
    mock_db_session.commit.assert_awaited_once()
    assert result == test_id


@pytest.mark.asyncio
async def test_delete_one(repo, mock_db_session):
    test_id = uuid4()

    mock_result = MagicMock()
    mock_result.scalar_one.return_value = test_id
    mock_db_session.execute.return_value = mock_result

    result = await repo.delete_one(test_id)

    mock_db_session.execute.assert_called_once()
    mock_db_session.commit.assert_awaited_once()
    assert result == test_id


@pytest.mark.asyncio
async def test_find_one(repo, mock_db_session):
    test_fields = ['id', 'name']
    test_filter = {'name': 'test'}
    test_result = {'id': uuid4(), 'name': 'test'}

    mock_result = MagicMock()
    mock_result.mappings.return_value.first.return_value = test_result
    mock_db_session.execute.return_value = mock_result

    result = await repo.find_one(test_fields, test_filter)

    mock_db_session.execute.assert_called_once()
    assert result == test_result


@pytest.mark.asyncio
async def test_find_all(repo, mock_db_session):
    test_fields = ['id', 'value']
    test_filter = {'value': 100}
    test_order = 'id'
    test_limit = 10

    test_data = [
        {'id': uuid4(), 'value': 100},
        {'id': uuid4(), 'value': 100}
    ]

    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = test_data
    mock_db_session.execute.return_value = mock_result

    result = await repo.find_all(
        test_fields,
        filter_by=test_filter,
        order_by=test_order,
        limit=test_limit
    )

    mock_db_session.execute.assert_called_once()
    assert len(result) == 2
    assert all('id' in item and 'value' in item for item in result)
    assert result == test_data
