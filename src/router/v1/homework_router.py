from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from services import HomeworkService
from typing import Annotated, List, Union, Dict
from schemas import (
    ShortActiveHomework,
    ShortLastHomework,
    ActiveHomework,
    LastHomework,
    TeacherHomework,
    CreateHomework,
    EditHomework,
    TaskHomeworkSubmit,
    VariantStatistic
)
from dependecies import get_current_user, get_homework_service
from exceptions import NotFoundException, NoRightsException, IncorrectDataException


router = APIRouter(tags=['Homework'])


@router.post('', response_model=UUID)
async def create_homework(
        homework_data: CreateHomework,
        payload: Annotated[Dict, Depends(get_current_user)],
        homework_service: Annotated[HomeworkService, Depends(get_homework_service)]
):
    """Создание нового домашнего задания.

    :param homework_data: Данные нового задания.
    :param payload: JWT payload текущего пользователя.
    :param homework_service: Сервис работы с заданиями.

    :return: Идентификатор созданного задания.

    :raises HTTPException 403: Нет прав на создание домашнего задания."""
    try:
        hw_id = await homework_service.create_homework(homework_data, payload['role'])
        return hw_id
    except NoRightsException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e.name))


@router.get('', response_model=List[Union[ShortActiveHomework, ShortLastHomework]])
async def get_homework(
        active: bool,
        payload: Annotated[Dict, Depends(get_current_user)],
        homework_service: Annotated[HomeworkService, Depends(get_homework_service)]
):
    """Получение списка домашних заданий по статусу активности.

    :param active: Флаг фильтрации по активности.
    :param payload: JWT payload текущего пользователя.
    :param homework_service: Сервис для работы с заданиями.

    :return: Список домашних заданий.

    :raises HTTPException 404: Задания не найдены."""
    try:
        return await homework_service.get_homeworks_by_user(UUID(payload['sub']), active)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.name))


@router.get('/{homework_id}/active', response_model=ActiveHomework)
async def get_active_homework(
        homework_id: UUID,
        payload: Annotated[Dict, Depends(get_current_user)],
        homework_service: Annotated[HomeworkService, Depends(get_homework_service)]
):
    """Получение активного домашнего задания.

    :param homework_id: Идентификатор домашнего задания.
    :param payload: JWT payload текущего пользователя.
    :param homework_service: Сервис работы с заданиями.

    :return: Подробности активного задания.

    :raises HTTPException 403: Нет прав.
    :raises HTTPException 404: Задание не найдено.
    :raises HTTPException 400: Неверные данные."""
    try:
        return await homework_service.get_active_homework(homework_id, UUID(payload['sub']), payload['role'])
    except NoRightsException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e.name))
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.name))
    except IncorrectDataException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.name))


@router.get('/{homework_id}/completed', response_model=LastHomework)
async def get_completed_homework(
        homework_id: UUID,
        payload: Annotated[Dict, Depends(get_current_user)],
        homework_service: Annotated[HomeworkService, Depends(get_homework_service)]
):
    """Получение завершенного домашнего задания.

    :param homework_id: Идентификатор домашнего задания.
    :param payload: JWT payload текущего пользователя.
    :param homework_service: Сервис работы с заданиями.

    :return: Подробности активного задания.

    :raises HTTPException 403: Нет прав.
    :raises HTTPException 404: Задание не найдено.
    :raises HTTPException 400: Неверные данные."""
    try:
        return await homework_service.get_completed_homework(homework_id, UUID(payload['sub']), payload['role'])
    except NoRightsException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e.name))
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.name))
    except IncorrectDataException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.name))


@router.get('/{homework_id}', response_model=TeacherHomework)
async def get_homework(
        homework_id: UUID,
        payload: Annotated[Dict, Depends(get_current_user)],
        homework_service: Annotated[HomeworkService, Depends(get_homework_service)]
):
    """Получение домашнего задания для преподавателя.

    :param homework_id: Идентификатор задания.
    :param payload: JWT payload текущего пользователя.
    :param homework_service: Сервис работы с заданиями.

    :return: Полные данные задания.

    :raises HTTPException 403: Нет прав.
    :raises HTTPException 404: Задание не найдено."""
    try:
        return await homework_service.get_homework(homework_id, payload['role'])
    except NoRightsException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e.name))
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.name))


@router.patch('/{homework_id}', response_model=UUID)
async def update_homework(
        homework_id: UUID,
        homework_data: EditHomework,
        payload: Annotated[Dict, Depends(get_current_user)],
        homework_service: Annotated[HomeworkService, Depends(get_homework_service)]
):
    """Обновление информации о домашнем задании.

    :param homework_id: Идентификатор редактируемого задания.
    :param homework_data: Новые данные.
    :param payload: JWT payload текущего пользователя.
    :param homework_service: Сервис работы с заданиями.

    :return: Идентификатор обновленного задания.

    :raises HTTPException 403: Нет прав."""
    try:
        return await homework_service.edit_homework(homework_id, homework_data, payload['role'])
    except NoRightsException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e.name))


@router.delete('/{homework_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_homework(
        homework_id: UUID,
        payload: Annotated[Dict, Depends(get_current_user)],
        homework_service: Annotated[HomeworkService, Depends(get_homework_service)]
):
    """Удаление домашнего задания.

    :param homework_id: Идентификатор удаляемого задания.
    :param payload: JWT payload текущего пользователя.
    :param homework_service: Сервис работы с заданиями.

    :raises HTTPException 403: Нет прав."""
    try:
        return await homework_service.delete_homework(homework_id, payload['role'])
    except NoRightsException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e.name))


@router.post('/{homework_id}/submit', response_model=LastHomework)
async def submit_homework(
        homework_id: UUID,
        data: List[TaskHomeworkSubmit],
        payload: Annotated[Dict, Depends(get_current_user)],
        homework_service: Annotated[HomeworkService, Depends(get_homework_service)]
):
    """Отправка домашнего задания на проверку.

    :param homework_id: Идентификатор задания.
    :param data: Решенные упражнения.
    :param payload: JWT payload текущего пользователя.
    :param homework_service: Сервис работы с заданиями.

    :return: Завершенное задание.

    :raises HTTPException 403: Нет прав.
    :raises HTTPException 404: Задание не найдено."""
    try:
        return await homework_service.submit_homework(homework_id, data, UUID(payload['sub']), payload['role'])
    except NoRightsException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e.name))
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.name))


@router.get('/{homework_id}/statistic', response_model=List[VariantStatistic])
async def get_homework_statistic(
        homework_id: UUID,
        payload: Annotated[Dict, Depends(get_current_user)],
        homework_service: Annotated[HomeworkService, Depends(get_homework_service)]
):
    """Получение успешности выполнения задания по вариантам упражнения.

    :param homework_id: Идентификатор задания.
    :param payload: JWT payload текущего пользователя.
    :param homework_service: Сервис работы с заданиями.

    :return: Список статистики выполнения по вариантам.

    :raises HTTPException 403: Нет прав."""
    try:
        return await homework_service.get_statistic(homework_id, payload['role'])
    except NoRightsException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e.name))
