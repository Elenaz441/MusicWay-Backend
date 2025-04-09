from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
from pathlib import Path


class RunConfig(BaseModel):
    host: str = '127.0.0.1'
    port: int = 8000


class ApiV1Prefix(BaseModel):
    prefix: str = '/v1'
    auth: str = '/auth'
    users: str = '/users'
    topic_block: str = '/topic-blocks'
    material: str = '/materials'
    feedback: str = '/feedbacks'
    variant: str = '/variants'
    task: str = '/tasks'
    homework: str = '/homeworks'
    classes: str = '/classes'


class ApiPrefix(BaseModel):
    prefix: str = '/api'
    v1: ApiV1Prefix = ApiV1Prefix()


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool

    naming_convention: dict[str, str] = {
        'ix': 'ix_%(column_0_label)s',
        'uq': 'uq_%(table_name)s_%(column_0_N_name)s',
        'ck': 'ck_%(table_name)s_%(constraint_name)s',
        'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
        'pk': 'pk_%(table_name)s',
    }


class RedisConfig(BaseModel):
    host: str
    port: int
    password: str


class AuthConfig(BaseModel):
    secret_key: str
    token_url: str = '/api/v1/auth/login'
    lifetime_seconds_access: int = 3600
    lifetime_seconds_refresh: int = 86400
    algorithm: str = 'HS256'


class EmailSenderConfig(BaseModel):
    host: str
    user: str
    password: str
    port: int
    template_folder: str = Path(__file__).parent / 'templates/emails'


class FrontendConfig(BaseModel):
    url: str


class S3Config(BaseModel):
    key_id: str
    secret: str
    bucket_name: str
    endpoint_url: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=('.env.template', '.env'),
        case_sensitive=False,
        env_nested_delimiter='__',
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig
    redis: RedisConfig
    auth: AuthConfig
    email_sender: EmailSenderConfig
    front: FrontendConfig
    s3: S3Config


settings = Settings()

BASE_DIR = Path(__file__).resolve().parent.parent

