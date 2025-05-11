import pytest
from uuid import uuid4

from services.class_service import ClassService
from schemas import ShortClassResponse, ClassResponse, ShortLastHWTeacher, HomeworkStatistic
from exceptions import NoRightsException, NotFoundException


@pytest.fixture
def class_service(mock_class_repo, mock_students_repo, mock_user_repo, mock_homework_repo):
    return ClassService(
        class_repo=mock_class_repo,
        students_repo=mock_students_repo,
        user_repo=mock_user_repo,
        homework_repo=mock_homework_repo
    )


@pytest.mark.asyncio
async def test_get_classes_success(class_service):
    teacher_id = uuid4()
    class_data = [{'id': uuid4(), 'class_number': 5, 'week_day': 'Понедельник', 'class_time': '10:00'}]
    class_service.class_repo.find_all.return_value = class_data

    result = await class_service.get_classes(teacher_id, role='Преподаватель')

    assert isinstance(result, list)
    assert all(isinstance(c, ShortClassResponse) for c in result)
    assert result[0].class_number == 5
    assert result[0].week_day == 'Понедельник'


@pytest.mark.asyncio
async def test_get_classes_forbidden(class_service):
    with pytest.raises(NoRightsException):
        await class_service.get_classes(uuid4(), role='Ученик')


@pytest.mark.asyncio
async def test_get_class_by_id_success(class_service: ClassService):
    class_id = uuid4()
    teacher_id = uuid4()
    student_id = uuid4()

    class_service.class_repo.find_one.return_value = {
        'id': class_id,
        'class_number': 5,
        'week_day': 'Понедельник',
        'class_time': '10:00',
        'teacher_id': teacher_id,
    }
    students = [{'student_id': student_id}, {'student_id': uuid4()}]
    class_service.students_repo.find_all.return_value = students
    class_service.user_repo.find_one.return_value = {
        'id': student_id,
        'name': 'Иван',
        'surname': 'Иванов',
        'patronymic': 'Иванович',
    }
    class_service.homework_repo.find_all_active.return_value = [{
        'id': uuid4(),
        'topic': 'Test',
        'end_date': '2025-06-09',
        'max_mark': 30,
        'start_date': '2025-05-09',
        'count': 10
    }]

    result = await class_service.get_class_by_id(class_id, teacher_id, role='Преподаватель')

    assert isinstance(result, ClassResponse)
    assert result.id == class_id
    assert result.class_number == 5
    assert result.students[0].name == 'Иван'
    assert result.active_homeworks[0].count == 5


@pytest.mark.asyncio
async def test_get_class_by_id_not_found(class_service):
    class_service.class_repo.find_one.return_value = None

    with pytest.raises(NotFoundException):
        await class_service.get_class_by_id(uuid4(), uuid4(), role='Преподаватель')


@pytest.mark.asyncio
async def test_get_class_by_id_forbidden_wrong_role(class_service):
    with pytest.raises(NoRightsException):
        await class_service.get_class_by_id(uuid4(), uuid4(), role='Ученик')


@pytest.mark.asyncio
async def test_get_class_by_id_forbidden_wrong_teacher(class_service):
    class_obj = {'teacher_id': uuid4()}
    class_service.class_repo.find_one.return_value = class_obj

    with pytest.raises(NoRightsException):
        await class_service.get_class_by_id(uuid4(), uuid4(), role='Преподаватель')


@pytest.mark.asyncio
async def test_get_last_homeworks_success(class_service):
    class_id = uuid4()
    teacher_id = uuid4()
    class_service.class_repo.find_one.return_value = {'teacher_id': teacher_id}
    hw_data = [{'id': uuid4(), 'topic': 'HW 1'}]
    class_service.homework_repo.find_all_completed.return_value = hw_data

    result = await class_service.get_last_homeworks(class_id, teacher_id, role='Преподаватель')

    assert isinstance(result, list)
    assert all(isinstance(hw, ShortLastHWTeacher) for hw in result)
    assert result[0].topic == 'HW 1'


@pytest.mark.asyncio
async def test_get_last_homeworks_no_rights(class_service):
    with pytest.raises(NoRightsException):
        await class_service.get_last_homeworks(uuid4(), uuid4(), role='Ученик')


@pytest.mark.asyncio
async def test_get_last_homeworks_class_not_found(class_service):
    class_service.class_repo.find_one.return_value = None

    with pytest.raises(NotFoundException):
        await class_service.get_last_homeworks(uuid4(), uuid4(), role='Преподаватель')


@pytest.mark.asyncio
async def test_get_last_homeworks_wrong_teacher(class_service):
    class_service.class_repo.find_one.return_value = {'teacher_id': uuid4()}

    with pytest.raises(NoRightsException):
        await class_service.get_last_homeworks(uuid4(), uuid4(), role='Преподаватель')


@pytest.mark.asyncio
async def test_get_statistic_success(class_service):
    class_id = uuid4()
    stats_data = [{'id': uuid4(), 'topic': 'Test', 'success_rate': 12}]
    class_service.homework_repo.get_statistic.return_value = stats_data

    result = await class_service.get_statistic(class_id, role='Преподаватель')

    assert isinstance(result, list)
    assert all(isinstance(s, HomeworkStatistic) for s in result)
    assert result[0].topic == 'Test'
    assert result[0].success_rate == 12


@pytest.mark.asyncio
async def test_get_statistic_no_rights(class_service):
    with pytest.raises(NoRightsException):
        await class_service.get_statistic(uuid4(), role='Ученик')
