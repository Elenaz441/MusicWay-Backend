from sqladmin.authentication import AuthenticationBackend
from fastapi import Request, HTTPException
import jwt
from config import settings
from datetime import datetime, timezone
from dependecies import get_auth_service
from exceptions import IncorrectDataException
from database import get_async_session, get_redis_async_session
from starlette.responses import RedirectResponse


class AdminAuth(AuthenticationBackend):
    """Кастомная аутентификация для SQLAdmin"""

    def __init__(self):
        super().__init__(secret_key=settings.auth.secret_key)
        self.db = None
        self.redis = None
        self.auth_service = None

    async def setup(self):
        async for session in get_async_session():
            self.db = session
            break

        async for session in get_redis_async_session():
            self.redis = session
            break

        self.auth_service = await get_auth_service(self.db, self.redis)

    async def login(self, request: Request) -> RedirectResponse:
        """Обрабатывает логин через форму SQLAdmin."""
        form = await request.form()
        email = form.get('username')
        password = form.get('password')

        if not email or not password:
            raise HTTPException(status_code=400, detail='Введите email и пароль.')

        try:
            token = await self.auth_service.login_user(email, password)
            access_token = token.access_token
        except IncorrectDataException as e:
            raise HTTPException(status_code=401, detail=str(e))

        response = RedirectResponse(url='/admin', status_code=302)
        request.session.update({'token': access_token})
        return response

    async def authenticate(self, request: Request) -> bool:
        """Авторизация пользователя в админке."""
        token = request.session.get('token')

        if not token:
            return False

        try:
            payload = jwt.decode(token, settings.auth.secret_key, algorithms=['HS256'])
            exp = payload.get('exp')
            role = payload.get('role')
            if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
                return False

            if role != 'Админ':
                return False

            return True

        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False

    async def logout(self, request: Request) -> RedirectResponse:
        """Выход из системы."""
        token = request.session.get('token')
        await self.auth_service.invalidate_token(token)
        request.session.clear()

        return RedirectResponse(url='/admin/login', status_code=302)
