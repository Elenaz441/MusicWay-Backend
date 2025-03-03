from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from redis import Redis
from repositories import UserRepository, RoleRepository
from fastapi.security import OAuth2PasswordBearer
from config import settings
from services import AuthService
from database import get_async_session, get_redis_async_session
from typing import Annotated


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.auth.token_url)


async def get_auth_service(
    db: Annotated[AsyncSession, Depends(get_async_session)],
    redis: Annotated[Redis, Depends(get_redis_async_session)]
) -> AuthService:
    """Глобальная зависимость для AuthService."""
    return AuthService(UserRepository(db), RoleRepository(db), redis)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    """Проверяет и декодирует JWT-токен."""
    try:
        payload = await auth_service.decode_jwt(token)
        return payload
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
