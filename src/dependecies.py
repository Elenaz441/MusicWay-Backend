from typing import Annotated

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from database import get_async_session, get_redis_async_session
from exceptions import InvalidTokenException
from repositories import (
    UserRepository,
    RoleRepository,
    TopicBlockRepository,
    MaterialRepository,
    FeedbackRepository,
    VariantRepository
)
from services import (
    AuthService,
    TopicBlockService,
    MaterialService,
    FeedbackService,
    VariantService
)

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
    except InvalidTokenException as e:
        raise HTTPException(status_code=401, detail=str(e.name))


async def get_topic_block_service(
    db: Annotated[AsyncSession, Depends(get_async_session)]
) -> TopicBlockService:
    """Глобальная зависимость для TopicBlockService."""
    return TopicBlockService(TopicBlockRepository(db))


async def get_material_service(
        db: Annotated[AsyncSession, Depends(get_async_session)]
) -> MaterialService:
    """Глобальная зависимость для MaterialService."""
    return MaterialService(MaterialRepository(db))


async def get_feedback_service(
        db: Annotated[AsyncSession, Depends(get_async_session)]
) -> FeedbackService:
    """Глобальная зависимость для FeedbackService."""
    return FeedbackService(FeedbackRepository(db), MaterialRepository(db))


async def get_variant_service(
        db: Annotated[AsyncSession, Depends(get_async_session)]
) -> VariantService:
    """Глобальная зависимость VariantService."""
    return VariantService(VariantRepository(db))
