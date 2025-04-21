from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from repositories import MelodyRepo
from services import SettingService, TaskService
from database import get_async_session
from typing import Annotated


async def get_setting_service(
    db: Annotated[AsyncSession, Depends(get_async_session)]
) -> SettingService:
    """Глобальная зависимость для SettingService."""
    return SettingService(MelodyRepo(db))


async def get_task_service(
    db: Annotated[AsyncSession, Depends(get_async_session)]
) -> TaskService:
    """Глобальная зависимость для TaskService."""
    return TaskService(MelodyRepo(db))
