import pytest
from unittest.mock import patch
from uuid import UUID, uuid4
from datetime import datetime, timedelta, timezone
import jwt

from config import settings
from schemas import UserRegister, TokenResponse
from exceptions import (
    NoRightsException,
    AlreadyExistsException,
    IncorrectDataException,
    InvalidTokenException
)
from services import AuthService


@pytest.fixture
def auth_service(mock_user_repo, mock_role_repo, mock_redis):
    return AuthService(mock_user_repo, mock_role_repo, mock_redis)


@pytest.fixture
def sample_user_data():
    return UserRegister(
        email='tests@example.com',
        password='Password123!',
        name='Test',
        surname='User',
        patronymic='Patronymic',
        birthdate='2000-01-01',
        role='Ученик'
    )


@pytest.fixture
def sample_token_payload():
    return {
        'sub': str(uuid4()),
        'role': 'Ученик',
        'exp': datetime.now(timezone.utc) + timedelta(minutes=30)
    }


@pytest.mark.asyncio
async def test_generate_jwt(auth_service):
    payload = {'sub': str(1), 'role': 'Test'}
    token = auth_service.generate_jwt(payload, timedelta(minutes=5))
    decoded = jwt.decode(token, settings.auth.secret_key, algorithms=[settings.auth.algorithm])
    assert decoded['sub'] == '1'
    assert decoded['role'] == 'Test'
    assert 'exp' in decoded


@patch('jwt.decode', return_value={'exp': int((datetime.now(timezone.utc) + timedelta(seconds=60)).timestamp())})
@pytest.mark.asyncio
async def test_invalidate_token_success(mock_jwt_decode, auth_service):
    await auth_service.invalidate_token('some_token')
    auth_service.redis.setex.assert_called_once()
    args, kwargs = auth_service.redis.setex.call_args
    assert args[0] == 'blacklist:some_token'
    assert args[2] == 'true'


@pytest.mark.asyncio
async def test_register_user_success(auth_service, sample_user_data):
    uuid = uuid4()
    auth_service.user_repo.find_one.return_value = None
    auth_service.role_repo.find_one.return_value = {'id': uuid}
    auth_service.user_repo.add_one.return_value = uuid

    result = await auth_service.register_user(sample_user_data)

    assert isinstance(result, UUID)
    assert uuid == result
    auth_service.user_repo.find_one.assert_awaited_once_with(['id'], {'email': sample_user_data.email})
    auth_service.role_repo.find_one.assert_awaited_once_with(['id'], {'name': sample_user_data.role})


@pytest.mark.asyncio
async def test_register_user_already_exists(auth_service, sample_user_data):
    auth_service.user_repo.find_one.return_value = {'id': uuid4()}

    with pytest.raises(AlreadyExistsException) as exc_info:
        await auth_service.register_user(sample_user_data)

    assert 'пользователь' in str(exc_info.value)
    assert 'email' in str(exc_info.value)


@pytest.mark.asyncio
async def test_login_user_success(auth_service):
    test_email = 'tests@example.com'
    test_password = 'Password123!'
    hashed_password = 'hashed_password'

    user_mock = {
        'id': uuid4(),
        'email': test_email,
        'name': 'Test',
        'surname': 'User',
        'role_id': uuid4(),
        'hashed_password': hashed_password,
        'is_changed_password': False
    }

    role_mock = {'name': 'Ученик'}

    auth_service.user_repo.find_one.return_value = user_mock
    auth_service.role_repo.find_one.return_value = role_mock

    with patch('services.auth_service.verify_password', return_value=True), \
            patch.object(auth_service, 'generate_jwt', side_effect=['access.token', 'refresh.token']):
        result = await auth_service.login_user(test_email, test_password)

        assert isinstance(result, TokenResponse)
        assert result.access_token == 'access.token'
        assert result.refresh_token == 'refresh.token'
        assert result.role == 'Ученик'
        assert result.name == 'Test'


@pytest.mark.asyncio
async def test_login_user_incorrect_credentials(auth_service):
    auth_service.user_repo.find_one.return_value = None

    with pytest.raises(IncorrectDataException) as exc_info:
        await auth_service.login_user('wrong@example.com', 'wrongpass')

    assert 'Неверный email или пароль' in str(exc_info.value)


@pytest.mark.asyncio
async def test_refresh_token_success(auth_service, sample_token_payload):
    test_refresh_token = 'refresh.token'
    user_mock = {
        'name': 'Test',
        'is_changed_password': False
    }

    auth_service.redis.exists.return_value = False
    auth_service.user_repo.find_one.return_value = user_mock

    with patch('jwt.decode', return_value=sample_token_payload), \
            patch.object(auth_service, 'generate_jwt', side_effect=['new.access.token', 'new.refresh.token']):
        result = await auth_service.refresh_token(test_refresh_token)

        assert isinstance(result, TokenResponse)
        assert result.access_token == 'new.access.token'
        assert result.refresh_token == 'new.refresh.token'
        assert result.role == 'Ученик'
        assert result.name == 'Test'


@pytest.mark.asyncio
async def test_refresh_token_blacklisted(auth_service):
    test_refresh_token = 'blacklisted.token'
    auth_service.redis.exists.return_value = True

    with pytest.raises(IncorrectDataException) as exc_info:
        await auth_service.refresh_token(test_refresh_token)

    assert 'Токен недействителен' in str(exc_info.value)


@pytest.mark.asyncio
async def test_refresh_token_expired(auth_service):
    test_refresh_token = 'expired.token'
    auth_service.redis.exists.return_value = False

    with patch('jwt.decode', side_effect=jwt.ExpiredSignatureError()), \
            pytest.raises(IncorrectDataException) as exc_info:
        await auth_service.refresh_token(test_refresh_token)

    assert 'Refresh-токен истек' in str(exc_info.value)


@pytest.mark.asyncio
async def test_change_password_success(auth_service):
    user_id = uuid4()
    role_name = 'Преподаватель'
    new_password = 'New_password123!'

    await auth_service.change_password(user_id, role_name, new_password)

    auth_service.user_repo.edit_one.assert_called_once()
    args, kwargs = auth_service.user_repo.edit_one.call_args
    assert args[0] == user_id
    assert 'hashed_password' in args[1]
    assert args[1]['is_changed_password'] is True


@pytest.mark.asyncio
async def test_change_password_no_rights(auth_service):
    user_id = uuid4()
    role_name = 'Ученик'
    new_password = 'New_password123!'
    with pytest.raises(NoRightsException):
        await auth_service.change_password(user_id, role_name, new_password)


@pytest.mark.asyncio
async def test_decode_jwt_success(auth_service, sample_token_payload):
    test_token = 'valid.token'
    auth_service.redis.exists.return_value = False

    with patch('jwt.decode', return_value=sample_token_payload):
        result = await auth_service.decode_jwt(test_token)

        assert result == sample_token_payload


@pytest.mark.asyncio
async def test_decode_jwt_blacklisted(auth_service):
    test_token = 'blacklisted.token'
    auth_service.redis.exists.return_value = True

    with pytest.raises(InvalidTokenException) as exc_info:
        await auth_service.decode_jwt(test_token)

    assert 'Токен недействителен' in str(exc_info.value)


@pytest.mark.asyncio
async def test_decode_jwt_expired(auth_service):
    test_token = 'expired.token'
    auth_service.redis.exists.return_value = False

    with patch('jwt.decode', side_effect=jwt.ExpiredSignatureError()), \
            pytest.raises(InvalidTokenException) as exc_info:
        await auth_service.decode_jwt(test_token)

    assert 'Токен истёк' in str(exc_info.value)


@pytest.mark.asyncio
async def test_decode_jwt_invalid(auth_service):
    test_token = 'invalid.token'
    auth_service.redis.exists.return_value = False

    with patch('jwt.decode', side_effect=jwt.InvalidTokenError()), \
            pytest.raises(InvalidTokenException) as exc_info:
        await auth_service.decode_jwt(test_token)

    assert 'Некорректный токен' in str(exc_info.value)
