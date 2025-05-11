import pytest
from uuid import uuid4, UUID
from services.feedback_service import FeedbackService
from exceptions import NoRightsException, NotFoundException
from schemas import CreateFeedback


@pytest.fixture
def feedback_service(mock_feedback_repo, mock_material_repo):
    return FeedbackService(
        feedback_repo=mock_feedback_repo,
        material_repo=mock_material_repo
    )


@pytest.mark.asyncio
async def test_create_feedback_success(feedback_service):
    material_id = uuid4()
    feedback_data = CreateFeedback(material_id=material_id, comment='Отличный материал!')
    feedback_service.feedback_repo.add_one.return_value = uuid4()
    feedback_service.material_repo.find_one.return_value = {'id': material_id}

    feedback_id = await feedback_service.create_feedback(feedback_data, role_name='Преподаватель')

    assert isinstance(feedback_id, UUID)
    feedback_service.material_repo.find_one.assert_awaited_once_with(['id'], {'id': material_id})
    feedback_service.feedback_repo.add_one.assert_awaited_once_with({
        'material_id': material_id,
        'comment': 'Отличный материал!'
    })


@pytest.mark.asyncio
async def test_create_feedback_no_rights(feedback_service):
    feedback_data = CreateFeedback(material_id=uuid4(), comment='Комментарий')

    with pytest.raises(NoRightsException):
        await feedback_service.create_feedback(feedback_data, role_name='Ученик')

    feedback_service.material_repo.find_one.assert_not_awaited()
    feedback_service.feedback_repo.add_one.assert_not_awaited()


@pytest.mark.asyncio
async def test_create_feedback_material_not_found(feedback_service):
    material_id = uuid4()
    feedback_data = CreateFeedback(material_id=material_id, comment='Комментарий')
    feedback_service.material_repo.find_one.return_value = None

    with pytest.raises(NotFoundException):
        await feedback_service.create_feedback(feedback_data, role_name='Преподаватель')

    feedback_service.material_repo.find_one.assert_awaited_once_with(['id'], {'id': material_id})
    feedback_service.feedback_repo.add_one.assert_not_awaited()
