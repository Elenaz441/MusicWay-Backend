import redis
import jwt
from uuid import UUID
from datetime import datetime, timedelta, timezone

from repositories import UserRepository, RoleRepository
from schemas import UserRegister, TokenResponse
from config import settings
from utils import hash_password, verify_password
from exceptions import NoRightsException, AlreadyExistsException, IncorrectDataException, InvalidTokenException


class AuthService:
    """Сервис для работы с авторизацией пользователей."""
    def __init__(self, user_repo: UserRepository, role_repo: RoleRepository, redis_client: redis.Redis):
        self.user_repo = user_repo
        self.role_repo = role_repo
        self.redis = redis_client

    def generate_jwt(self, data: dict, expires_delta: timedelta) -> str:
        """Генерация JWT-токена.

        :param data: Данные, которые нужно зашифровать.
        :param expires_delta: Время жизни токена.

        :return: JWT строка."""
        to_encode = data.copy()
        to_encode.update({'exp': datetime.now(timezone.utc) + expires_delta})
        return jwt.encode(to_encode, settings.auth.secret_key, algorithm=settings.auth.algorithm)

    async def invalidate_token(self, token: str):
        """Добавление токена в Redis Blacklist.

        :param token: JWT токен, который нужно инвалидировать."""
        exp = jwt.decode(token, settings.auth.secret_key, algorithms=[settings.auth.algorithm])['exp']
        ttl = exp - int(datetime.now(timezone.utc).timestamp())
        if ttl > 0:
            await self.redis.setex(f'blacklist:{token}', ttl, 'true')

    async def is_token_blacklisted(self, token: str) -> bool:
        """Проверка наличия токена в blacklist Redis.

        :param token: JWT токен.

        :return: True, если токен в blacklist, иначе False."""
        return await self.redis.exists(f'blacklist:{token}') > 0

    async def register_user(self, user_data: UserRegister) -> UUID:
        """Регистрация нового пользователя.

        :param user_data: Данные для регистрации пользователя.

        :return: UUID нового пользователя.

        :raises AlreadyExistsException: Если пользователь с таким email уже существует."""
        existing_user = await self.user_repo.find_one(['id'], {'email': user_data.email})
        if existing_user:
            raise AlreadyExistsException('пользователь', 'email')

        hashed_password = hash_password(user_data.password)
        role = await self.role_repo.find_one(['id'], {'name': user_data.role})
        new_user = {
            'email': user_data.email,
            'hashed_password': hashed_password,
            'name': user_data.name,
            'surname': user_data.surname,
            'patronymic': user_data.patronymic,
            'birthdate': user_data.birthdate,
            'role_id': role['id'],
            'is_changed_password': user_data.role == 'Ученик'
        }
        return await self.user_repo.add_one(new_user)

    async def login_user(self, email: str, password: str) -> TokenResponse:
        """Авторизация пользователя.

        :param email: Email пользователя.
        :param password: Пароль пользователя.

        :return: Access и Refresh токены.

        :raises IncorrectDataException: Неверный email или пароль."""
        user = await self.user_repo.find_one(
            ['id', 'email', 'name', 'role_id', 'hashed_password', 'is_changed_password'],
            {'email': email}
        )
        if not user or not verify_password(password, user['hashed_password']):
            raise IncorrectDataException('Неверный email или пароль')

        role = await self.role_repo.find_one(['name'], {'id': user['role_id']})
        payload = {'sub': str(user['id']), 'role': role['name']}

        access_token = self.generate_jwt(payload, timedelta(seconds=settings.auth.lifetime_seconds_access))
        refresh_token = self.generate_jwt(payload, timedelta(seconds=settings.auth.lifetime_seconds_refresh))
        response = TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            role=role['name'],
            name=user['name'],
            is_changed_password=user['is_changed_password']
        )

        return response

    async def refresh_token(self, refresh_token: str) -> TokenResponse:
        """Обновление Access- и Refresh- токенов на основе существующего Refresh токена.

        :param refresh_token: Refresh JWT токен.

        :return: Новые Access и Refresh токены.

        :raises IncorrectDataException: Если токен просрочен или недействителен."""
        if await self.is_token_blacklisted(refresh_token):
            raise IncorrectDataException('Токен недействителен')

        try:
            payload = jwt.decode(refresh_token, settings.auth.secret_key, algorithms=[settings.auth.algorithm])
        except jwt.ExpiredSignatureError:
            raise IncorrectDataException('Refresh-токен истек')

        access_token = self.generate_jwt(payload, timedelta(seconds=settings.auth.lifetime_seconds_access))
        refresh_token = self.generate_jwt(payload, timedelta(seconds=settings.auth.lifetime_seconds_refresh))
        user = await self.user_repo.find_one(['name', 'is_changed_password'], filter_by={'id': UUID(payload['sub'])})
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            role=payload['role'],
            name=user['name'],
            is_changed_password=user['is_changed_password']
        )

    async def change_password(self, user_id: UUID, role_name: str, new_password: str):
        """Смена пароля преподавателя при первой авторизации.

        :param user_id: Идентификатор пользователя.
        :param role_name: Название роли пользователя.
        :param new_password: Новый пароль.

        :raises NoRightsException: Если роль не имеет права на смену пароля."""
        if role_name not in ['Преподаватель', 'Админ']:
            raise NoRightsException()
        hashed_password = hash_password(new_password)
        await self.user_repo.edit_one(user_id, {'hashed_password': hashed_password, 'is_changed_password': True})

    async def decode_jwt(self, token: str):
        """Декодирует JWT, проверяет срок действия и наличие в blacklist.

        :param token: JWT токен.

        :return: Раскодированные данные из токена.

        :raises InvalidTokenException: Если токен просрочен, некорректен или в blacklist."""
        if await self.is_token_blacklisted(token):
            raise InvalidTokenException('Токен недействителен')

        try:
            return jwt.decode(token, settings.auth.secret_key, algorithms=[settings.auth.algorithm])
        except jwt.ExpiredSignatureError:
            raise InvalidTokenException('Токен истёк')
        except jwt.InvalidTokenError:
            raise InvalidTokenException('Некорректный токен')
