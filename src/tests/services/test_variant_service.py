import pytest
from unittest.mock import patch
from uuid import uuid4
from services import VariantService
from exceptions import NotFoundException
from schemas import VariantResponse, VariantListResponse


@pytest.fixture
def variant_service(mock_variant_repo, mock_task_type_repo, mock_block_repo):
    return VariantService(
        variant_repo=mock_variant_repo,
        task_type_repo=mock_task_type_repo,
        block_repo=mock_block_repo
    )


@pytest.mark.asyncio
async def test_get_variants_by_block_none(variant_service):
    block_id = None
    role = 'Ученик'
    variant_service.block_repo.find_all.return_value = [{'id': uuid4(), 'name': 'Интервалы'}]
    variant_service.variant_repo.find_all_by_block.return_value = [{
        'id': uuid4(),
        'name': 'Вариант 1',
        'image_url': 'url',
        'student_description': 'описание для ученика',
        'teacher_description': 'описание для учителя',
        'demo_url': 'demo',
        'for_homework': True
    }]

    result = await variant_service.get_variants_by_block(block_id, role)

    assert isinstance(result, list)
    assert isinstance(result[0], VariantListResponse)
    assert result[0].variants[0].description == 'описание для ученика'


@pytest.mark.asyncio
async def test_get_variants_by_block_teacher_filtering(variant_service):
    block_id = None
    role = 'Преподаватель'
    variant_service.block_repo.find_all.return_value = [{'id': uuid4(), 'name': 'Интервалы'}]
    variant_service.variant_repo.find_all_by_block.return_value = [
        {
            'id': uuid4(),
            'name': 'Вариант 1',
            'image_url': 'url',
            'student_description': 'ученик 1',
            'teacher_description': 'учитель 1',
            'demo_url': 'demo',
            'for_homework': False
        },
        {
            'id': uuid4(),
            'name': 'Вариант 2',
            'image_url': 'url',
            'student_description': 'ученик 2',
            'teacher_description': 'учитель 2',
            'demo_url': 'demo2',
            'for_homework': True
        }
    ]

    result = await variant_service.get_variants_by_block(block_id, role)

    assert len(result[0].variants) == 1
    assert result[0].variants[0].description == 'учитель 2'


@pytest.mark.asyncio
@patch('services.variant_service.send_query')
async def test_get_variant_success(mock_send_query, variant_service):
    variant_id = uuid4()
    role = 'Ученик'

    variant_service.variant_repo.find_one.return_value = {
        'id': variant_id,
        'name': 'Вариант A',
        'student_description': 'описание 1',
        'teacher_description': 'описание 2',
        'demo_url': 'demo',
        'task_type_id': uuid4()
    }
    variant_service.task_type_repo.find_one.return_value = {'service_url': 'http://example.com'}
    mock_send_query.return_value = {'setting_1': True}

    result = await variant_service.get_variant(variant_id, role)

    assert isinstance(result, VariantResponse)
    assert result.description == 'описание 1'
    assert result.settings == {'setting_1': True}


@pytest.mark.asyncio
async def test_get_variant_not_found(variant_service):
    variant_service.variant_repo.find_one.return_value = None

    with pytest.raises(NotFoundException):
        await variant_service.get_variant(variant_id=uuid4(), role='Ученик')
