import pytest
from uuid import uuid4
from services.setting_service import SettingService
from schemas import MelodySettingResponse


@pytest.fixture
def setting_service(mock_melody_repo):
    return SettingService(repo=mock_melody_repo)


@pytest.mark.asyncio
async def test_get_setting_for_teacher(setting_service):
    setting_service.repo.find_all.return_value = [
        {'id': uuid4(), 'name': 'Мелодия 1'},
        {'id': uuid4(), 'name': 'Мелодия 2'}
    ]

    response = await setting_service.get_setting(role='Преподаватель')

    assert isinstance(response, MelodySettingResponse)
    assert response.description == 'Выберите мелодии, которые хотите задать:'
    assert len(response.melodies) == 2
    assert response.melodies[0].name == 'Мелодия 1'
    assert response.melodies[1].name == 'Мелодия 2'
    assert response.is_need_count is False
    setting_service.repo.find_all.assert_awaited_once_with(['id', 'name'])


@pytest.mark.asyncio
async def test_get_setting_for_student(setting_service):
    response = await setting_service.get_setting(role='Ученик')

    assert isinstance(response, MelodySettingResponse)
    assert response.description is None
    assert response.melodies is None
    assert response.is_need_count is False
    setting_service.repo.find_all.assert_not_awaited()
