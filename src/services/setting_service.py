from schemas import IntervalsSettingResponse


class SettingService:
    """Сервер для работы с настройками"""

    async def get_settings(self) -> IntervalsSettingResponse:
        return IntervalsSettingResponse()
