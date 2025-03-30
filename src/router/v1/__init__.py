from fastapi import APIRouter

from config import settings

from .auth_router import router as auth_router
from .topic_block_router import router as topic_block_router
from .material_router import router as material_router
from .feedback_router import router as feedback_router
from .variant_router import router as variant_router
from .task_router import router as task_router
from .homework_router import router as homework_router
from .class_router import router as class_router
from .user_router import router as user_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)
router.include_router(auth_router, prefix=settings.api.v1.auth)
router.include_router(user_router, prefix=settings.api.v1.users)
router.include_router(topic_block_router, prefix=settings.api.v1.topic_block)
router.include_router(material_router, prefix=settings.api.v1.material)
router.include_router(feedback_router, prefix=settings.api.v1.feedback)
router.include_router(variant_router, prefix=settings.api.v1.variant)
router.include_router(task_router, prefix=settings.api.v1.task)
router.include_router(class_router, prefix=settings.api.v1.classes)
router.include_router(homework_router, prefix=settings.api.v1.homework)
