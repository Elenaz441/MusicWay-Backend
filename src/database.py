from typing import AsyncGenerator
import redis

from config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker


engine = create_async_engine(str(settings.db.url), echo=True)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


redis_session = redis.asyncio.StrictRedis(host=settings.redis.host,
                                         port=settings.redis.port,
                                         password=settings.redis.password,
                                         decode_responses=True)


async def get_redis_async_session() -> AsyncGenerator[redis.Redis, None]:
    async with redis_session as session:
        yield session
