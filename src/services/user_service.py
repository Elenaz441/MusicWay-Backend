from repositories import TopicBlockRepository, StudentClassRepository, HomeworkRepository
from schemas import UserStatistic
from exceptions import NoRightsException, NotFoundException
from uuid import UUID


class UserService:
    """Сервис для работы с пользователями."""
    def __init__(
            self,
            block_repo: TopicBlockRepository,
            student_class_repo: StudentClassRepository,
            homework_repo: HomeworkRepository
    ):
        self.block_repo = block_repo
        self.student_class_repo = student_class_repo
        self.homework_repo = homework_repo

    async def get_statistic(self, user_id: UUID, role: str) -> UserStatistic:
        """Получает процент успешности выполнения заданий.

        :param user_id: Идентификатор пользователя.
        :param role: Роль пользователя.

        :return: Процент успешности.

        :raises NoRightsException: Нет прав.
        """
        if role != 'Ученик':
            raise NoRightsException()
        blocks = await self.block_repo.find_all(['id', 'name', 'image_url'])

        class_id = await self.student_class_repo.find_one(['class_id'], {'student_id': user_id})
        if not class_id:
            raise NotFoundException('класс', 'user_id')
        tasks = await self.homework_repo.find_all_completed({'class_id': class_id.class_id, 'student_id': user_id})
        student_mark = 0
        max_mark = 0
        for task in tasks:
            print(task.student_mark, task.max_mark)
            student_mark += task.student_mark
            max_mark += task.max_mark
        success_rate = student_mark * 100 // max_mark
        return UserStatistic(success_rate=success_rate, topic_blocks=blocks)
