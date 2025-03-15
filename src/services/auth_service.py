import redis
import bcrypt
import jwt
from uuid import UUID
from datetime import datetime, timedelta, timezone

from repositories import UserRepository, RoleRepository
from schemas import UserRegister, TokenResponse
from config import settings
from exceptions import NoRightsException, AlreadyExistsException, IncorrectDataException, InvalidTokenException


class AuthService:
    """Сервис для работы с авторизацией пользователей."""
    def __init__(self, user_repo: UserRepository, role_repo: RoleRepository, redis_client: redis.Redis):
        self.user_repo = user_repo
        self.role_repo = role_repo
        self.redis = redis_client

    def hash_password(self, password: str) -> str:
        """Хеширование пароля перед сохранением."""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Проверка введенного пароля с хешем из БД."""
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

    def generate_jwt(self, data: dict, expires_delta: timedelta) -> str:
        """Генерация JWT-токена."""
        to_encode = data.copy()
        to_encode.update({'exp': datetime.now(timezone.utc) + expires_delta})
        return jwt.encode(to_encode, settings.auth.secret_key, algorithm=settings.auth.algorithm)

    async def invalidate_token(self, token: str):
        """Добавление токена в Redis Blacklist."""
        exp = jwt.decode(token, settings.auth.secret_key, algorithms=[settings.auth.algorithm])['exp']
        ttl = exp - int(datetime.now(timezone.utc).timestamp())
        if ttl > 0:
            await self.redis.setex(f'blacklist:{token}', ttl, 'true')

    async def is_token_blacklisted(self, token: str) -> bool:
        """Проверка наличия токена в blacklist Redis."""
        return await self.redis.exists(f'blacklist:{token}') > 0

    async def register_user(self, user_data: UserRegister) -> UUID:
        """Регистрация нового пользователя."""
        existing_user = await self.user_repo.find_one(['id'], {'email': user_data.email})
        if existing_user:
            raise AlreadyExistsException('пользователь', 'email')

        hashed_password = self.hash_password(user_data.password)
        role = await self.role_repo.find_one(['id'], {'name': user_data.role})
        new_user = {
            'email': user_data.email,
            'hashed_password': hashed_password,
            'name': user_data.name,
            'surname': user_data.surname,
            'patronymic': user_data.patronymic,
            'birthdate': user_data.birthdate,
            'role_id': role.id
        }
        return await self.user_repo.add_one(new_user)

    async def login_user(self, email: str, password: str) -> TokenResponse:
        """Авторизация пользователя."""
        user = await self.user_repo.find_one(
            ['id', 'email', 'role_id', 'hashed_password', 'is_first_login'],
            {'email': email}
        )
        if not user or not self.verify_password(password, user.hashed_password):
            raise IncorrectDataException('Неверный email или пароль')

        role = await self.role_repo.find_one(['name'], {'id': user.role_id})
        payload = {'sub': str(user.id), 'role': role.name, 'is_first_login': user.is_first_login}

        if user.is_first_login:
            await self.user_repo.edit_one(user.id, {'is_first_login': False})

        access_token = self.generate_jwt(payload, timedelta(seconds=settings.auth.lifetime_seconds_access))
        refresh_token = self.generate_jwt(payload, timedelta(seconds=settings.auth.lifetime_seconds_refresh))

        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    async def refresh_token(self, refresh_token: str) -> TokenResponse:
        """Обновление Access-токена."""
        if await self.is_token_blacklisted(refresh_token):
            raise IncorrectDataException('Токен недействителен')

        try:
            payload = jwt.decode(refresh_token, settings.auth.secret_key, algorithms=[settings.auth.algorithm])
        except jwt.ExpiredSignatureError:
            raise IncorrectDataException('Refresh-токен истек')

        access_token = self.generate_jwt(payload, timedelta(seconds=settings.auth.lifetime_seconds_access))
        refresh_token = self.generate_jwt(payload, timedelta(seconds=settings.auth.lifetime_seconds_refresh))
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    async def change_password(self, email: str, role_name: str, new_password: str):
        """Смена пароля преподавателя при первой авторизации"""
        if role_name != 'Преподаватель':
            raise NoRightsException()
        user = await self.user_repo.find_one(['id'], {'email': email})
        hashed_password = self.hash_password(new_password)
        await self.user_repo.edit_one(user.id, {'hashed_password': hashed_password})

    async def decode_jwt(self, token: str):
        """Декодирует JWT, проверяет срок действия и наличие в blacklist."""
        if await self.is_token_blacklisted(token):
            raise InvalidTokenException('Токен недействителен')

        try:
            return jwt.decode(token, settings.auth.secret_key, algorithms=[settings.auth.algorithm])
        except jwt.ExpiredSignatureError:
            raise InvalidTokenException('Токен истёк')
        except jwt.InvalidTokenError:
            raise InvalidTokenException('Некорректный токен')
