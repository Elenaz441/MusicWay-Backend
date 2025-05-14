import pytest
from services.setting_service import SettingService
from exceptions import NotFoundException
from schemas import IntervalsSettingResponse


@pytest.fixture
def setting_service(mock_setting_repo):
    return SettingService(repo=mock_setting_repo)


@pytest.mark.asyncio
@pytest.mark.parametrize('role,expected_description,is_need_count', [
    ('Преподаватель', 'Можете задать определённые простые интервалы, по умолчанию выбраны все:', True),
    ('Ученик', 'Выбери интервалы, которые ты хочешь тренировать. Если ничего не выбирать, то будут все сразу.', False),
])
async def test_get_setting_by_name_success(setting_service, role, expected_description, is_need_count):
    intervals = ['м.2', 'ч.1']
    setting_service.repo.find_one.return_value = {'values': intervals}

    result = await setting_service.get_setting_by_name(role)

    assert isinstance(result, IntervalsSettingResponse)
    assert result.description == expected_description
    assert result.intervals == intervals
    assert result.is_need_count == is_need_count
    setting_service.repo.find_one.assert_awaited_once_with(['values'], name='Интервалы')


@pytest.mark.asyncio
async def test_get_setting_by_name_not_found(setting_service):
    setting_service.repo.find_one.return_value = None

    with pytest.raises(NotFoundException) as exc_info:
        await setting_service.get_setting_by_name('Ученик')

    assert 'setting' in str(exc_info.value) and 'name' in str(exc_info.value)
    setting_service.repo.find_one.assert_awaited_once_with(['values'], name='Интервалы')
