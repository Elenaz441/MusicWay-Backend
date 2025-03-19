from fastapi import APIRouter, Depends, HTTPException, status
from services import AuthService
from typing import Annotated
from schemas import UserRegister, TokenResponse, RefreshTokenRequest, ChangePasswordRequest
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config import settings
from dependecies import get_auth_service, get_current_user
from exceptions import NoRightsException, AlreadyExistsException, IncorrectDataException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.auth.token_url)

router = APIRouter(tags=['Auth'])


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(
        user_data: UserRegister,
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    """Регистрация нового пользователя."""
    try:
        await auth_service.register_user(user_data)
        return {'message': 'Пользователь успешно зарегистрирован'}
    except AlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e.name))


@router.post('/login', response_model=TokenResponse)
async def login(
        user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    """Авторизация пользователя."""
    try:
        return await auth_service.login_user(user_data.username, user_data.password)
    except IncorrectDataException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.name))


@router.get('/login')
async def get_login_status(
        payload: Annotated[dict, Depends(get_current_user)]
):
    """Проверка статуса авторизации."""
    return {'message': 'Вы авторизованы', 'id': payload['sub'], 'role': payload['role']}


@router.post('/refresh', response_model=TokenResponse)
async def refresh_token(
        token_data: RefreshTokenRequest,
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    """Обновление Access-токена."""
    token = token_data.refresh_token
    try:
        data = await auth_service.refresh_token(token)
        await auth_service.invalidate_token(token)
        return data
    except IncorrectDataException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.name))


@router.delete('/logout')
async def logout(
        token: Annotated[str, Depends(oauth2_scheme)],
        payload: Annotated[dict, Depends(get_current_user)],
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    """Выход из системы (добавление токена в blacklist)."""
    await auth_service.invalidate_token(token)
    return {'message': 'Вы успешно вышли из системы'}


@router.patch('/change-password')
async def change_password(
        data: ChangePasswordRequest,
        payload: Annotated[dict, Depends(get_current_user)],
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    """Смена пароля"""
    try:
        await auth_service.change_password(payload['sub'], payload['role'], data.new_password)
        return {'message': 'Пароль успешно изменён.'}
    except NoRightsException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e.name))
