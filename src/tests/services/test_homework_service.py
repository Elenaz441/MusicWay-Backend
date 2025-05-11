import pytest
from uuid import uuid4
from datetime import date
from services.homework_service import HomeworkService
from exceptions import NotFoundException, NoRightsException, IncorrectDataException
from schemas import (
    TaskHomeworkSubmit, ShortActiveHomework, ShortLastHomework,
    ActiveHomework, LastHomework, TeacherHomework,
    CreateHomework, EditHomework, VariantStatistic
)
from unittest.mock import AsyncMock, patch


@pytest.fixture
def homework_service(mock_homework_repo, mock_students_repo, mock_task_repo,
                     mock_material_repo, mock_task_type_repo, mock_variant_repo, mock_hw_task_repo):
    return HomeworkService(
        homework_repo=mock_homework_repo,
        student_class_repo=mock_students_repo,
        task_repo=mock_task_repo,
        material_repo=mock_material_repo,
        task_type_repo=mock_task_type_repo,
        variant_repo=mock_variant_repo,
        hw_task_repo=mock_hw_task_repo
    )


@pytest.mark.asyncio
async def test_get_homeworks_by_user_active_success(homework_service):
    user_id = uuid4()
    class_id = {'class_id': uuid4()}
    homework_service.student_class_repo.find_one.return_value = class_id
    homework_service.homework_repo.find_all_active.return_value = [{
        'id': uuid4(),
        'topic': 'Test',
        'end_date': '2020-01-01',
        'max_mark': 10}]
    result = await homework_service.get_homeworks_by_user(user_id, active=True)

    assert isinstance(result, list)
    assert all(isinstance(c, ShortActiveHomework) for c in result)
    homework_service.student_class_repo.find_one.assert_awaited_once()
    homework_service.homework_repo.find_all_active.assert_awaited_once()
    homework_service.homework_repo.find_all_completed.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_homeworks_by_user_not_found(homework_service):
    homework_service.student_class_repo.find_one.return_value = None

    with pytest.raises(NotFoundException):
        await homework_service.get_homeworks_by_user(uuid4(), active=False)


@pytest.mark.asyncio
async def test_get_homeworks_by_user_last_success(homework_service):
    user_id = uuid4()
    class_id = {'class_id': uuid4()}
    homework_service.student_class_repo.find_one.return_value = class_id
    homework_service.homework_repo.find_all_completed.return_value = [{
        'id': uuid4(),
        'topic': 'Test',
        'student_mark': 7,
        'max_mark': 10}]
    result = await homework_service.get_homeworks_by_user(user_id, active=False)

    assert isinstance(result, list)
    assert all(isinstance(c, ShortLastHomework) for c in result)
    homework_service.student_class_repo.find_one.assert_awaited_once()
    homework_service.homework_repo.find_all_active.assert_not_awaited()
    homework_service.homework_repo.find_all_completed.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_active_homework_success(homework_service):
    user_id = uuid4()
    hw_id = uuid4()
    role = 'Ученик'

    homework_service.homework_repo.is_completed.return_value = False
    homework_service.homework_repo.find_one_with_mark.return_value = {
        'id': hw_id, 'topic': 'Topic', 'block': 'Block',
        'end_date': '2020-01-01', 'max_mark': 10, 'count': 2
    }
    homework_service.task_repo.find_all_by_homework.return_value = [{
        'variant_id': uuid4(),
        'name': 'Sing',
        'count': 2
    }]
    homework_service.material_repo.find_all_by_homework.return_value = [{
        'id': uuid4(),
        'name': 'Test',
        'number': 0
    }]

    result = await homework_service.get_active_homework(hw_id, user_id, role)

    assert isinstance(result, ActiveHomework)
    assert result.id == hw_id
    assert result.task_type_variants[0].name == 'Sing'
    assert result.task_type_variants[0].count == 2
    assert result.related_materials[0].number == 0
    homework_service.homework_repo.is_completed.assert_awaited_once()
    homework_service.homework_repo.find_one_with_mark.assert_awaited_once()
    homework_service.task_repo.find_all_by_homework.assert_awaited_once()
    homework_service.material_repo.find_all_by_homework.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_active_homework_wrong_role(homework_service):
    with pytest.raises(NoRightsException):
        await homework_service.get_active_homework(uuid4(), uuid4(), 'Преподаватель')


@pytest.mark.asyncio
async def test_get_active_homework_already_completed(homework_service):
    homework_service.homework_repo.is_completed.return_value = True
    with pytest.raises(IncorrectDataException):
        await homework_service.get_active_homework(uuid4(), uuid4(), 'Ученик')


@pytest.mark.asyncio
async def test_get_active_homework_not_found(homework_service):
    homework_service.homework_repo.is_completed.return_value = False
    homework_service.homework_repo.find_one_with_mark.return_value = None

    with pytest.raises(NotFoundException):
        await homework_service.get_active_homework(uuid4(), uuid4(), 'Ученик')


@pytest.mark.asyncio
async def test_get_completed_homework_success(homework_service):
    user_id = uuid4()
    hw_id = uuid4()
    role = 'Ученик'

    homework_service.homework_repo.is_completed.return_value = True
    homework_service.homework_repo.find_one_with_mark.return_value = {
        'id': hw_id, 'topic': 'Topic', 'block': 'Block',
        'end_date': '2020-01-01', 'student_mark': 12, 'max_mark': 20
    }
    homework_service.homework_repo.get_marks.return_value = [
        {'name': 'Тип 1', 'number': 1, 'student_mark': 5, 'max_mark': 10},
        {'name': 'Тип 1', 'number': 2, 'student_mark': 3, 'max_mark': 5},
        {'name': 'Тип 2', 'number': 3, 'student_mark': 4, 'max_mark': 5},
    ]

    result = await homework_service.get_completed_homework(hw_id, user_id, role)

    assert isinstance(result, LastHomework)
    assert len(result.task_type_variants) == 2
    assert result.task_type_variants[0].student_mark == 8
    assert result.task_type_variants[0].max_mark == 15
    assert len(result.task_type_variants[0].tasks) == 2
    assert result.task_type_variants[0].tasks[1].number == 2


@pytest.mark.asyncio
async def test_get_completed_homework_wrong_role(homework_service):
    with pytest.raises(NoRightsException):
        await homework_service.get_completed_homework(uuid4(), uuid4(), 'Преподаватель')


@pytest.mark.asyncio
async def test_get_completed_homework_not_completed(homework_service):
    homework_service.homework_repo.is_completed.return_value = False
    with pytest.raises(IncorrectDataException):
        await homework_service.get_completed_homework(uuid4(), uuid4(), 'Ученик')


@pytest.mark.asyncio
async def test_get_completed_homework_not_found(homework_service):
    homework_service.homework_repo.is_completed.return_value = True
    homework_service.homework_repo.find_one_with_mark.return_value = None
    with pytest.raises(NotFoundException):
        await homework_service.get_completed_homework(uuid4(), uuid4(), 'Ученик')


@pytest.mark.asyncio
async def test_get_homework_success(homework_service):
    hw_id = uuid4()
    role = 'Преподаватель'
    student1_id = uuid4()
    student2_id = uuid4()

    homework_service.homework_repo.get_homework_students.return_value = [
        {'id': student1_id,
         'name': 'Elle',
         'surname': 'Smit',
         'patronymic': None,
         'student_mark': 4},
        {'id': student2_id,
         'name': 'Sally',
         'surname': 'Smit',
         'patronymic': None,
         'student_mark': 5}
    ]
    homework_service.homework_repo.find_one_with_mark.return_value = {
        'id': hw_id, 'topic': 'Topic', 'block': 'Block',
        'end_date': date(year=2020, month=2, day=1), 'start_date': date(year=2020, month=1, day=1),
        'student_mark': 4, 'max_mark': 5, 'count': 5
    }
    homework_service.task_repo.find_all_by_homework.return_value = [
        {'variant_id': uuid4(), 'name': 'Sing', 'count': 5}
    ]
    homework_service.material_repo.find_all_by_homework.return_value = []
    homework_service.homework_repo.get_homework_tasks.return_value = [
        {'student_id': student1_id, 'task_name': 'Sing', 'student_mark': 4, 'max_mark': 5},
        {'student_id': student2_id, 'task_name': 'Sing', 'student_mark': 5, 'max_mark': 5}
    ]

    result = await homework_service.get_homework(hw_id, role)

    assert isinstance(result, TeacherHomework)
    assert result.is_completed
    assert len(result.related_materials) == 0
    assert len(result.task_type_variants) == 1
    assert result.task_type_variants[0].name == 'Sing'
    assert len(result.results) == 2
    assert len(result.results[0].tasks) == 1
    homework_service.homework_repo.get_homework_students.assert_awaited_once()
    homework_service.task_repo.find_all_by_homework.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_homework_wrong_role(homework_service):
    with pytest.raises(NoRightsException):
        await homework_service.get_homework(uuid4(), 'Ученик')


@pytest.mark.asyncio
async def test_get_homework_not_found(homework_service):
    homework_service.homework_repo.get_homework_students.return_value = [{'id': uuid4()}]
    homework_service.homework_repo.find_one_with_mark.return_value = None

    with pytest.raises(NotFoundException):
        await homework_service.get_homework(uuid4(), 'Преподаватель')


@pytest.mark.asyncio
async def test_create_homework_success(homework_service):
    data = CreateHomework(
        topic='Test',
        start_date=date.today(),
        end_date=date.today(),
        block_id=uuid4(),
        class_id=uuid4(),
        variants=[]
    )

    homework_service.homework_repo.add_one.return_value = {'id': uuid4()}
    result = await homework_service.create_homework(data, 'Преподаватель')

    assert isinstance(result, dict)
    homework_service.homework_repo.add_one.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_homework_wrong_role(homework_service):
    with pytest.raises(NoRightsException):
        await homework_service.create_homework(CreateHomework(
            topic='Test', start_date=date.today(), end_date=date.today(),
            block_id=uuid4(), class_id=uuid4(), variants=[]), 'Ученик')

    homework_service.homework_repo.add_one.assert_not_awaited()


@pytest.mark.asyncio
async def test_edit_homework_success(homework_service):
    hw_id = uuid4()
    data = EditHomework(topic='Updated topic')

    homework_service.homework_repo.find_one.return_value = {'id': hw_id}
    result = await homework_service.edit_homework(hw_id, data, 'Преподаватель')

    assert result == hw_id
    homework_service.homework_repo.edit_one.assert_awaited_once_with(hw_id, {'topic': 'Updated topic'})


@pytest.mark.asyncio
async def test_edit_homework_wrong_role(homework_service):
    with pytest.raises(NoRightsException):
        await homework_service.edit_homework(uuid4(), EditHomework(topic='Test'), 'Ученик')

    homework_service.homework_repo.edit_one.assert_not_awaited()


@pytest.mark.asyncio
async def test_delete_homework_success(homework_service):
    hw_id = uuid4()
    homework_service.homework_repo.find_one.return_value = {'id': hw_id}

    await homework_service.delete_homework(hw_id, 'Преподаватель')

    homework_service.homework_repo.delete_one.assert_awaited_once_with(hw_id)


@pytest.mark.asyncio
async def test_delete_homework_wrong_role(homework_service):
    with pytest.raises(NoRightsException):
        await homework_service.delete_homework(uuid4(), 'Ученик')

    homework_service.homework_repo.delete_one.assert_not_awaited()


@pytest.mark.asyncio
@patch('services.homework_service.send_query', new_callable=AsyncMock)
async def test_submit_homework_success(mock_send_query, homework_service):
    hw_id = uuid4()
    user_id = uuid4()
    task_id = uuid4()
    variant_id = uuid4()
    task_type_id = uuid4()
    hw_task_id = uuid4()
    service_url = "http://mocked-service"

    homework_service.homework_repo.find_one.return_value = {'id': hw_id}
    homework_service.task_repo.find_one.return_value = {
        'id': task_id, 'variant_id': variant_id, 'answer': 'до'
    }
    homework_service.variant_repo.find_one.return_value = {'task_type_id': task_type_id}
    homework_service.task_type_repo.find_one.return_value = {'service_url': service_url}
    homework_service.hw_task_repo.find_one.return_value = {'id': hw_task_id, 'student_id': user_id, 'task_id': task_id}
    homework_service.homework_repo.is_completed.return_value = True
    homework_service.homework_repo.find_one_with_mark.return_value = {
        'id': hw_id, 'topic': 'Topic', 'block': 'Block',
        'end_date': '2020-01-01', 'student_mark': 5, 'max_mark': 5
    }
    homework_service.homework_repo.get_marks.return_value = [
        {'name': 'Тип 1', 'number': 1, 'student_mark': 5, 'max_mark': 5}
    ]

    mock_send_query.return_value = {'mark': 5}

    submit_data = TaskHomeworkSubmit(
        task_id=task_id,
        check_data={'answer': 'до'}
    )

    result = await homework_service.submit_homework(hw_id, [submit_data], user_id, role='Ученик')

    assert len(result.task_type_variants) == 1
    assert result.student_mark == 5
    mock_send_query.assert_awaited_once_with(
        'POST',
        f'{service_url}/tasks/get-mark',
        {'check_data': {'answer': 'до'}, 'answer': 'до'}
    )
    homework_service.hw_task_repo.edit_one.assert_awaited_once_with(hw_task_id, {'mark': 5})


@pytest.mark.asyncio
async def test_submit_homework_wrong_role(homework_service):
    with pytest.raises(NoRightsException):
        await homework_service.submit_homework(uuid4(), [], uuid4(), 'Преподаватель')


@pytest.mark.asyncio
async def test_submit_homework_not_found(homework_service):
    homework_service.homework_repo.find_one.return_value = None

    with pytest.raises(NotFoundException):
        await homework_service.submit_homework(uuid4(), [], uuid4(), 'Ученик')


@pytest.mark.asyncio
async def test_get_statistic_success(homework_service):
    homework_id = uuid4()
    role = 'Преподаватель'

    homework_service.homework_repo.get_marks.return_value = [
        {'name': 'Вариант 1', 'student_mark': 40, 'max_mark': 50},
        {'name': 'Вариант 1', 'student_mark': 10, 'max_mark': 10},
        {'name': 'Вариант 2', 'student_mark': 25, 'max_mark': 50},
    ]

    result = await homework_service.get_statistic(homework_id, role)

    assert isinstance(result, list)
    assert all(isinstance(r, VariantStatistic) for r in result)
    assert len(result) == 2
    assert result[0].success_rate == 83
    assert result[1].success_rate == 50

    homework_service.homework_repo.get_marks.assert_awaited_once_with(homework_id)


@pytest.mark.asyncio
async def test_get_statistic_no_rights(homework_service):
    homework_id = uuid4()
    role = 'Ученик'

    with pytest.raises(NoRightsException):
        await homework_service.get_statistic(homework_id, role)

    homework_service.homework_repo.get_marks.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_statistic_empty_result(homework_service):
    homework_id = uuid4()
    role = 'Преподаватель'
    homework_service.homework_repo.get_marks.return_value = []

    result = await homework_service.get_statistic(homework_id, role)

    assert result == []
    homework_service.homework_repo.get_marks.assert_awaited_once_with(homework_id)
