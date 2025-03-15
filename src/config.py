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
    tag: str = 'Auth'
    prefix: str = '/auth'
    register: str = '/register'
    refresh: str = '/refresh'
    login: str = '/login'
    logout: str = '/logout'
    change_password: str = '/change-password'


class TopicBlockPrefix(BaseModel):
    tag: str = 'Topic blocks'
    prefix: str = '/topic-blocks'
    topic_blocks: str = ''
    statistic: str = '/{block_id}/statistic'


class MaterialPrefix(BaseModel):
    tag: str = 'Study materials'
    prefix: str = '/materials'
    materials: str = ''
    video: str = '/{material_id}/video'
    text: str = '/{material_id}/text'
    tasks: str = '/{material_id}/tasks'
    search: str = '/search'


class FeedbackPrefix(BaseModel):
    tag: str = 'Feedback'
    prefix: str = '/feedbacks'
    create_feedback: str = ''


class VariantPrefix(BaseModel):
    tag: str = 'Variants'
    prefix: str = '/variants'
    variants: str = ''
    variant: str = '/{variant_id}'


class TaskPrefix(BaseModel):
    tag: str = 'Tasks'
    prefix: str = '/tasks'
    create_task: str = ''
    get_by_id: str = '/{task_id}'
    get_by_homework: str = '/{homework_id}/{task_number}'
    get_by_material: str = '/{material_id}/{variant_id}/{task_number}'


class HomeworkPrefix(BaseModel):
    tag: str = 'Homeworks'
    prefix: str = '/homeworks'


class ApiV1Prefix(BaseModel):
    prefix: str = '/v1'
    users: str = '/users'
    auth: AuthApiPrefix = AuthApiPrefix()
    topic_block: TopicBlockPrefix = TopicBlockPrefix()
    material: MaterialPrefix = MaterialPrefix()
    feedback: FeedbackPrefix = FeedbackPrefix()
    variant: VariantPrefix = VariantPrefix()
    task: TaskPrefix = TaskPrefix()
    homework: HomeworkPrefix = HomeworkPrefix()


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
    redis: RedisConfig
    auth: AuthConfig
    front: FrontendConfig


settings = Settings()

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

