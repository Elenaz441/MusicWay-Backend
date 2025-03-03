from pydantic import BaseModel, Field, EmailStr
from datetime import date
from typing import Optional


class UserRegister(BaseModel):
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


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str
