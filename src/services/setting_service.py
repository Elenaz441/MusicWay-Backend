from repositories import SettingRepo
from exceptions import NotFoundException
from schemas import IntervalsSettingResponse


class SettingService:
    """Сервис для работы с настройками."""

    def __init__(self, repo: SettingRepo):
        self.repo = repo

    async def get_setting_by_name(self, role: str) -> IntervalsSettingResponse:
        """Получает настройки по разделу (имени).

        :param role: Роль пользователя.

        :return: Настройки.
        """
        settings = await self.repo.find_one(['values'], name='Интервалы')
        if not settings:
            raise NotFoundException('setting', 'name')
        description = 'Выбери интервалы, которые ты хочешь тренировать. Если ничего не выбирать, то будут все сразу.'
        if role == 'Преподаватель':
            description = 'Можете задать определённые простые интервалы, по умолчанию выбраны все:'
        return IntervalsSettingResponse(
            description=description,
            intervals=settings['values'],
            is_need_count=role == 'Преподаватель'
        )
