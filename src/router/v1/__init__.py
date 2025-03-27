from fastapi import APIRouter

from config import settings

from .setting_router import router as setting_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)
router.include_router(setting_router, prefix=settings.api.v1.settings)
