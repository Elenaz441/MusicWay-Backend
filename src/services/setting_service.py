from repositories import MelodyRepo
from schemas import MelodySettingResponse


class SettingService:
    """Сервис для работы с настройками."""

    def __init__(self, repo: MelodyRepo):
        self.repo = repo

    async def get_setting(self, role: str) -> MelodySettingResponse:
        """Получает настройки.

        :param role: Роль пользователя.

        :return: Настройки.
        """
        melodies = await self.repo.find_all(['id', 'name'])
        description = 'Выберите мелодии, которые хотите задать:'
        if role != 'Преподаватель':
            description = melodies = None
        return MelodySettingResponse(
            description=description,
            melodies=melodies,
            is_need_count=False
        )
