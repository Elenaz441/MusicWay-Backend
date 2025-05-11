import pytest
from uuid import uuid4
from services import MaterialService
from exceptions import NotFoundException
from schemas import ShortMaterialResponse, MaterialVideoResponse, MaterialTextResponse, MaterialTasksResponse


@pytest.fixture
def material_service(mock_material_repo, mock_task_repo):
    return MaterialService(
        material_repo=mock_material_repo,
        task_repo=mock_task_repo
    )


@pytest.mark.asyncio
async def test_get_materials_by_block_success(material_service):
    block_id = uuid4()
    material_service.material_repo.find_all.return_value = [
        {'id': uuid4(), 'name': 'Материал 1', 'number': 1},
        {'id': uuid4(), 'name': 'Материал 2', 'number': 2},
    ]

    result = await material_service.get_materials_by_block(block_id)

    assert len(result) == 2
    assert all(isinstance(r, ShortMaterialResponse) for r in result)
    material_service.material_repo.find_all.assert_awaited_once_with(
        ['id', 'name', 'number'],
        filter_by={'block_id': block_id},
        order_by='number'
    )


@pytest.mark.asyncio
async def test_get_video_success(material_service):
    material_id = uuid4()
    material_service.material_repo.find_one.return_value = {
        'name': 'Видео урок',
        'video_url': 'http://example.com/video.mp4'
    }

    result = await material_service.get_video(material_id)

    assert isinstance(result, MaterialVideoResponse)
    assert result.name == 'Видео урок'
    assert result.video_url == 'http://example.com/video.mp4'
    material_service.material_repo.find_one.assert_awaited_once_with(
        ['name', 'video_url'],
        {'id': material_id}
    )


@pytest.mark.asyncio
async def test_get_video_not_found(material_service):
    material_service.material_repo.find_one.return_value = None
    with pytest.raises(NotFoundException):
        await material_service.get_video(uuid4())


@pytest.mark.asyncio
async def test_get_text_success(material_service):
    material_id = uuid4()
    material_service.material_repo.find_one.return_value = {
        'name': 'Теория',
        'text': 'Содержимое текста'
    }

    result = await material_service.get_text(material_id)

    assert isinstance(result, MaterialTextResponse)
    assert result.text == 'Содержимое текста'
    material_service.material_repo.find_one.assert_awaited_once_with(['name', 'text'], {'id': material_id})


@pytest.mark.asyncio
async def test_get_text_not_found(material_service):
    material_service.material_repo.find_one.return_value = None

    with pytest.raises(NotFoundException):
        await material_service.get_text(uuid4())


@pytest.mark.asyncio
async def test_get_tasks_success(material_service):
    material_id = uuid4()
    material_service.material_repo.find_one.return_value = {'name': 'Материал с упражнениями'}

    material_service.task_repo.find_all_by_material.return_value = [
        {'variant_id': uuid4(), 'name': 'Вариант A', 'count': 5},
        {'variant_id': uuid4(), 'name': 'Вариант B', 'count': 3},
    ]

    result = await material_service.get_tasks(material_id)

    assert isinstance(result, MaterialTasksResponse)
    assert result.name == 'Материал с упражнениями'
    assert len(result.variants) == 2
    material_service.material_repo.find_one.assert_awaited_once()
    material_service.task_repo.find_all_by_material.assert_awaited_once_with(material_id)


@pytest.mark.asyncio
async def test_get_tasks_not_found(material_service):
    material_service.material_repo.find_one.return_value = []

    with pytest.raises(NotFoundException):
        await material_service.get_tasks(uuid4())


@pytest.mark.asyncio
async def test_search_materials_success(material_service):
    query = 'интервалы'
    material_service.material_repo.find_all.return_value = [
        {'id': uuid4(), 'name': 'Прима', 'number': 1},
        {'id': uuid4(), 'name': 'Секунда', 'number': 2},
    ]

    result = await material_service.search_materials(query)

    assert len(result) == 2
    assert all(isinstance(r, ShortMaterialResponse) for r in result)
    material_service.material_repo.find_all.assert_awaited_once_with(
        ['id', 'name', 'number'],
        filter_by={'search_vector': query},
        limit=5
    )
