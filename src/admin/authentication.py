from sqladmin.authentication import AuthenticationBackend
from fastapi import Request, HTTPException, status
import jwt
from config import settings
from datetime import datetime, timezone
from dependecies import get_auth_service
from exceptions import IncorrectDataException
from database import get_async_session, get_redis_async_session
from starlette.responses import RedirectResponse


class AdminAuth(AuthenticationBackend):
    """Кастомный бэкенд аутентификации для SQLAdmin.

    Обеспечивает:

    - Аутентификацию через JWT
    - Ролевую проверку (только для админов)
    - Инвалидацию токенов
    - Управление сессиями

    :ivar db: Асинхронная сессия SQLAlchemy
    :ivar redis: Асинхронная сессия Redis
    :ivar auth_service: Сервис аутентификации"""

    def __init__(self):
        super().__init__(secret_key=settings.auth.secret_key)
        self.db = None
        self.redis = None
        self.auth_service = None

    async def setup(self):
        """Устанавливает асинхронные подключения к БД и Redis."""
        async for session in get_async_session():
            self.db = session
            break

        async for session in get_redis_async_session():
            self.redis = session
            break

        self.auth_service = await get_auth_service(self.db, self.redis)

    async def login(self, request: Request) -> RedirectResponse:
        """Обрабатывает аутентификацию через форму входа.

        :param request: Запрос с данными формы.

        :return: Редирект после успешной аутентификации.

        :raises HTTPException: При ошибках аутентификации (400, 401)."""
        form = await request.form()
        email = form.get('username')
        password = form.get('password')

        if not email or not password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Введите email и пароль.')

        try:
            token = await self.auth_service.login_user(email, password)
            access_token = token.access_token
        except IncorrectDataException as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

        response = RedirectResponse(url='/admin', status_code=status.HTTP_302_FOUND)
        request.session.update({'token': access_token})
        return response

    async def authenticate(self, request: Request) -> bool:
        """Проверяет аутентификацию и права доступа.

        :param request: Входящий запрос.

        :return: Результат проверки доступа."""
        token = request.session.get('token')

        if not token:
            return False

        try:
            payload = jwt.decode(token, settings.auth.secret_key, algorithms=[settings.auth.algorithm])
            role = payload.get('role')
            if role != 'Админ':
                return False
            exp = payload.get('exp')
            if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
                return False
            return True

        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return False

    async def logout(self, request: Request) -> RedirectResponse:
        """Обрабатывает выход из системы.

        :param request: Входящий запрос.

        :return: Редирект на страницу входа.
        """
        token = request.session.get('token')
        await self.auth_service.invalidate_token(token)
        request.session.clear()

        return RedirectResponse(url='/admin/login', status_code=status.HTTP_302_FOUND)
