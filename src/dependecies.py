from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from repositories import SettingRepo
from services import SettingService
from database import get_async_session
from typing import Annotated


async def get_setting_service(
    db: Annotated[AsyncSession, Depends(get_async_session)]
) -> SettingService:
    """Глобальная зависимость для SettingService."""
    return SettingService(SettingRepo(db))
