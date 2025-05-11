import pytest
from uuid import uuid4
from services.user_service import UserService
from schemas import UserStatistic
from exceptions import NoRightsException, NotFoundException


@pytest.fixture
def user_service(mock_block_repo, mock_students_repo, mock_homework_repo):
    return UserService(
        block_repo=mock_block_repo,
        student_class_repo=mock_students_repo,
        homework_repo=mock_homework_repo
    )


@pytest.mark.asyncio
async def test_get_statistic_raises_no_rights(user_service):
    with pytest.raises(NoRightsException):
        await user_service.get_statistic(user_id=uuid4(), role='Преподаватель')


@pytest.mark.asyncio
async def test_get_statistic_class_not_found(user_service):
    user_service.student_class_repo.find_one.return_value = None

    with pytest.raises(NotFoundException):
        await user_service.get_statistic(user_id=uuid4(), role='Ученик')


@pytest.mark.asyncio
async def test_get_statistic_no_tasks(user_service):
    user_id = uuid4()
    class_id = uuid4()

    user_service.block_repo.find_all.return_value = [
        {'id': uuid4(), 'name': 'Интервалы', 'image_url': 'url1'},
        {'id': uuid4(), 'name': 'Аккорды', 'image_url': 'url2'}
    ]
    user_service.student_class_repo.find_one.return_value = {'class_id': class_id}
    user_service.homework_repo.find_all_completed.return_value = []

    result = await user_service.get_statistic(user_id=user_id, role='Ученик')

    assert result.success_rate is None
    assert len(result.topic_blocks) == 2


@pytest.mark.asyncio
async def test_get_statistic_with_tasks(user_service):
    user_id = uuid4()
    class_id = uuid4()
    user_service.block_repo.find_all.return_value = []

    user_service.student_class_repo.find_one.return_value = {'class_id': class_id}

    user_service.homework_repo.find_all_completed.return_value = [
        {'student_mark': 8, 'max_mark': 10},
        {'student_mark': 7, 'max_mark': 10}
    ]

    result = await user_service.get_statistic(user_id=user_id, role='Ученик')

    assert isinstance(result, UserStatistic)
    assert result.success_rate == 75
    assert result.topic_blocks == []
