from fastapi import APIRouter, Depends

from services import SettingService
from typing import Annotated
from schemas import IntervalsSettingResponse
from dependecies import get_setting_service


router = APIRouter(tags=['Settings'])


@router.get('', response_model=IntervalsSettingResponse)
async def get_settings(
        setting_service: Annotated[SettingService, Depends(get_setting_service)]
):
    """Получение всех настроек."""
    return await setting_service.get_setting_by_name()
