import os
from unittest.mock import patch
import pytest
from unittest.mock import AsyncMock


@pytest.fixture(autouse=True, scope="session")
def mock_settings_env_vars():
    """Мокируем все необходимые переменные окружения для Settings"""
    mock_env = {
        # Database
        'DB__URL': 'postgresql+asyncpg://test:test@localhost:5432/test',
        'DB__ECHO': 'False',

        # Main service
        'MAIN__URL': 'http://localhost:3000',
    }

    with patch.dict(os.environ, mock_env):
        yield


@pytest.fixture
def mock_audio_repo():
    return AsyncMock()


@pytest.fixture
def mock_setting_repo():
    return AsyncMock()
