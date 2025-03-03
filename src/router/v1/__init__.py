from fastapi import APIRouter

from config import settings

# from .user import router as user_router
from .auth_router import router as auth_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)
# router.include_router(user_router, prefix=settings.api.v1.users,)
router.include_router(auth_router, prefix=settings.api.v1.auth.prefix)
