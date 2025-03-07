from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence

from models import TopicBlock


class TopicBlockRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_topic_blocks(self) -> Sequence[TopicBlock]:
        """Поиск всех разделов."""
        result = await self.db.execute(select(TopicBlock))
        return result.scalars().all()
