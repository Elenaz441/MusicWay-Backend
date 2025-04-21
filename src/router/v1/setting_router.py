from fastapi import APIRouter, Depends

from services import SettingService
from typing import Annotated
from schemas import MelodySettingResponse
from dependecies import get_setting_service


router = APIRouter(tags=['Settings'])


@router.get('', response_model=MelodySettingResponse)
async def get_settings(
        role: str,
        setting_service: Annotated[SettingService, Depends(get_setting_service)]
):
    """Получение всех настроек.

    :param role: Роль пользователя.
    :param setting_service: Сервис настроек.

    :return: Список настроек для упражнения.
    """
    return await setting_service.get_setting(role)
