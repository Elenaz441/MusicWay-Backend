from pydantic import Field, EmailStr, field_validator
import re
from datetime import date
from typing import Optional
from .base import PyBaseModel


class UserRegister(PyBaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=30)
    name: str = Field(min_length=2, max_length=100)
    surname: str = Field(min_length=2, max_length=100)
    patronymic: Optional[str] = Field(min_length=2, max_length=100)
    birthdate: date
    role: Optional[str] = Field(default='Ученик')

    @field_validator('password')
    @classmethod
    def validate_password(cls, value):
        """Проверяет пароль по требованиям безопасности."""
        if not re.search(r'[A-Z]', value):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву.')

        if not re.search(r'\d', value):
            raise ValueError('Пароль должен содержать хотя бы одну цифру.')

        if not re.search(r'[~!?@#$%^&*\-_+()\[\]{}></\\|"\'.:,]', value):
            raise ValueError('Пароль должен содержать хотя бы один специальный символ.')

        return value


class TokenResponse(PyBaseModel):
    access_token: str
    refresh_token: str


class RefreshTokenRequest(PyBaseModel):
    refresh_token: str


class ChangePasswordRequest(PyBaseModel):
    new_password: str = Field(min_length=8, max_length=30)
