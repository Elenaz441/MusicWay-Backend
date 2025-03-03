from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class RunConfig(BaseModel):
    host: str = '127.0.0.1'
    port: int = 8000


class AuthApiPrefix(BaseModel):
    prefix: str = '/auth'
    register: str = '/register'
    refresh: str = '/refresh'


class ApiV1Prefix(BaseModel):
    prefix: str = '/v1'
    users: str = '/users'
    auth: AuthApiPrefix = AuthApiPrefix()


class ApiPrefix(BaseModel):
    prefix: str = '/api'
    v1: ApiV1Prefix = ApiV1Prefix()


class DatabaseConfig(BaseModel):
    url: PostgresDsn

    naming_convention: dict[str, str] = {
        'ix': 'ix_%(column_0_label)s',
        'uq': 'uq_%(table_name)s_%(column_0_N_name)s',
        'ck': 'ck_%(table_name)s_%(constraint_name)s',
        'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
        'pk': 'pk_%(table_name)s',
    }


class AuthConfig(BaseModel):
    secret_key: str
    token_url: str = '/api/v1/auth/login'
    lifetime_seconds_access: int = 3600
    lifetime_seconds_refresh: int = 86400
    auth_by_email_chars_count: int = 6
    lifetime_seconds_code: int = 300


class FrontendConfig(BaseModel):
    url: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=('.env.template', '.env'),
        case_sensitive=False,
        env_nested_delimiter='__',
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig
    auth: AuthConfig
    front: FrontendConfig


settings = Settings()

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

