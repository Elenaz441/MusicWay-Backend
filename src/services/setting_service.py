from repositories import SettingRepo
from exceptions import NotFoundException
from schemas import IntervalsSettingResponse


class SettingService:
    """Сервис для работы с настройками."""

    def __init__(self, repo: SettingRepo):
        self.repo = repo

    async def get_setting_by_name(self) -> IntervalsSettingResponse:
        """Получает настройки по разделу (имени)."""
        settings = await self.repo.find_one(['values'], name='Интервалы')
        if not settings:
            raise NotFoundException('setting', 'name')
        res = dict(settings)
        print(type(res['values']))
        return IntervalsSettingResponse(intervals=res['values'])
