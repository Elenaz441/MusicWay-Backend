import pytest
from uuid import uuid4
from services.topic_block_service import TopicBlockService
from schemas import TopicBlockResponse, VariantStatistic
from exceptions import NoRightsException, NotFoundException


@pytest.fixture
def block_service(mock_block_repo, mock_students_repo, mock_homework_repo, mock_variant_repo):
    return TopicBlockService(
        block_repo=mock_block_repo,
        student_class_repo=mock_students_repo,
        homework_repo=mock_homework_repo,
        variant_repo=mock_variant_repo
    )


@pytest.mark.asyncio
async def test_get_blocks_returns_list(block_service):
    block_service.block_repo.find_all.return_value = [
        {'id': uuid4(), 'name': 'Интервалы', 'image_url': 'url1'},
        {'id': uuid4(), 'name': 'Аккорды', 'image_url': 'url2'}
    ]

    result = await block_service.get_blocks()
    assert isinstance(result, list)
    assert all(isinstance(b, TopicBlockResponse) for b in result)
    assert result[0].name == 'Интервалы'


@pytest.mark.asyncio
async def test_get_statistic_role_check(block_service):
    with pytest.raises(NoRightsException):
        await block_service.get_statistic(uuid4(), uuid4(), role='Преподаватель')


@pytest.mark.asyncio
async def test_get_statistic_class_not_found(block_service):
    block_service.student_class_repo.find_one.return_value = None
    with pytest.raises(NotFoundException):
        await block_service.get_statistic(uuid4(), uuid4(), role='Ученик')


@pytest.mark.asyncio
async def test_get_statistic_success(block_service):
    user_id = uuid4()
    block_id = uuid4()
    class_id = uuid4()

    block_service.student_class_repo.find_one.return_value = {'class_id': class_id}
    block_service.homework_repo.find_all_completed.return_value = [
        {'id': uuid4()},
        {'id': uuid4()}
    ]
    block_service.homework_repo.get_marks.side_effect = [
        [{'name': 'A', 'student_mark': 5, 'max_mark': 10}],
        [{'name': 'A', 'student_mark': 2, 'max_mark': 10}]
    ]
    block_service.variant_repo.find_all_by_block.return_value = [
        {'name': 'A'}, {'name': 'B'}
    ]

    result = await block_service.get_statistic(block_id, user_id, role='Ученик')

    assert isinstance(result, list)
    assert all(isinstance(b, VariantStatistic) for b in result)
    assert any(r.name == 'A' and r.success_rate == 35 for r in result)
    assert any(r.name == 'B' and r.success_rate == 0 for r in result)
