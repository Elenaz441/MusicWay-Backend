from pydantic import Field, EmailStr
from datetime import date
from typing import Optional
from .base import PyBaseModel


class UserRegister(PyBaseModel):
    email: EmailStr
    # password: str = Field(min_length=8, max_length=30, pattern=r'^(?=.*[A-Z])(?=.*\d)(?=.*[~!?@#$%^&*\-_+\(\)\[\]{'
    #                                                            r'}><\/\\|\"\'.:,])[a-zA-Z\d~!?@#$%^&*\-_+\(\)\[\]{'
    #                                                            r'}><\/\\|\"\'.:,]+$')
    password: str = Field(min_length=8, max_length=30)
    name: str = Field(min_length=2, max_length=100)
    surname: str = Field(min_length=2, max_length=100)
    patronymic: Optional[str] = Field(min_length=2, max_length=100)
    birthdate: date
    role: Optional[str] = Field(default='Ученик')


class TokenResponse(PyBaseModel):
    access_token: str
    refresh_token: str


class RefreshTokenRequest(PyBaseModel):
    refresh_token: str


class ChangePasswordRequest(PyBaseModel):
    new_password: str = Field(min_length=8, max_length=30)
