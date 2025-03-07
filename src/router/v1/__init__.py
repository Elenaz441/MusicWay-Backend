from fastapi import APIRouter

from config import settings

# from .user import router as user_router
from .auth_router import router as auth_router
from .topic_block_router import router as topic_block_router
from .material_router import router as material_router
from .feedback_router import router as feedback_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)
# router.include_router(user_router, prefix=settings.api.v1.users,)
router.include_router(auth_router, prefix=settings.api.v1.auth.prefix)
router.include_router(topic_block_router, prefix=settings.api.v1.topic_block.prefix)
router.include_router(material_router, prefix=settings.api.v1.material.prefix)
router.include_router(feedback_router, prefix=settings.api.v1.feedback.prefix)
