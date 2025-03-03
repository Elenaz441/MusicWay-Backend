from fastapi import APIRouter, Depends, HTTPException, status
from services.auth_service import AuthService
from typing import Annotated
from schemas import UserRegister, TokenResponse, RefreshTokenRequest
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config import settings
from dependecies import get_auth_service, get_current_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.auth.token_url)

router = APIRouter(tags=['Auth'])


@router.post(settings.api.v1.auth.register, status_code=status.HTTP_201_CREATED)
async def register(
        user_data: UserRegister,
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    """Регистрация нового пользователя."""
    try:
        await auth_service.register_user(user_data)
        return {'message': 'Пользователь успешно зарегистрирован'}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post(settings.api.v1.auth.login, response_model=TokenResponse)
async def login(
        user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    """Авторизация пользователя."""
    try:
        return await auth_service.login_user(user_data.username, user_data.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(settings.api.v1.auth.login)
async def get_login_status(
        payload: Annotated[dict, Depends(get_current_user)]
):
    """Проверка статуса авторизации (требуется передача JWT в заголовке)."""
    return {'message': 'Вы авторизованы', 'email': payload['sub'], 'role': payload['role']}


@router.post(settings.api.v1.auth.refresh, response_model=TokenResponse)
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
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(settings.api.v1.auth.logout)
async def logout(
        token: Annotated[str, Depends(oauth2_scheme)],
        payload: Annotated[dict, Depends(get_current_user)],
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    """Выход из системы (добавление токена в blacklist)."""
    await auth_service.invalidate_token(token)
    return {'message': 'Вы успешно вышли из системы'}
