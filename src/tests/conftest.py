import os
from unittest.mock import patch
import pytest
from pathlib import Path
from unittest.mock import AsyncMock


@pytest.fixture(autouse=True, scope="session")
def mock_settings_env_vars():
    """Мокируем все необходимые переменные окружения для Settings"""
    mock_env = {
        # Database
        'DB__URL': 'postgresql+asyncpg://test:test@localhost:5432/test',
        'DB__ECHO': 'False',

        # Redis
        'REDIS__HOST': 'localhost',
        'REDIS__PORT': '6379',
        'REDIS__PASSWORD': 'testpass',

        # Auth
        'AUTH__SECRET_KEY': 'test-secret-key',
        'AUTH__LIFETIME_SECONDS_ACCESS': '3600',
        'AUTH__LIFETIME_SECONDS_REFRESH': '86400',
        'AUTH__ALGORITHM': 'HS256',

        # Email
        'EMAIL_SENDER__HOST': 'smtp.test.com',
        'EMAIL_SENDER__USER': 'test@test.com',
        'EMAIL_SENDER__PASSWORD': 'testpass',
        'EMAIL_SENDER__PORT': '587',
        'EMAIL_SENDER__TEMPLATE_FOLDER': str(Path(__file__).parent / 'templates/emails'),

        # Frontend
        'FRONT__URL': 'http://localhost:3000',

        # S3
        'S3__KEY_ID': 'test-key-id',
        'S3__SECRET': 'test-secret',
        'S3__BUCKET_NAME': 'test-bucket',
        'S3__ENDPOINT_URL': 'http://localhost:9000',
    }

    with patch.dict(os.environ, mock_env):
        yield


@pytest.fixture
def mock_user_repo():
    return AsyncMock()


@pytest.fixture
def mock_role_repo():
    return AsyncMock()


@pytest.fixture
def mock_class_repo():
    return AsyncMock()


@pytest.fixture
def mock_students_repo():
    return AsyncMock()


@pytest.fixture
def mock_homework_repo():
    return AsyncMock()


@pytest.fixture
def mock_feedback_repo():
    return AsyncMock()


@pytest.fixture
def mock_material_repo():
    return AsyncMock()


@pytest.fixture
def mock_task_repo():
    return AsyncMock()


@pytest.fixture
def mock_task_type_repo():
    return AsyncMock()


@pytest.fixture
def mock_variant_repo():
    return AsyncMock()


@pytest.fixture
def mock_hw_task_repo():
    return AsyncMock()


@pytest.fixture
def mock_block_repo():
    return AsyncMock()


@pytest.fixture
def mock_redis():
    return AsyncMock()
