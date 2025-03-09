from repositories import AbstractRepository
from schemas import TopicBlockResponse
from typing import List


class TopicBlockService:
    """Сервис для работы с разделами."""
    def __init__(self, block_repo: AbstractRepository):
        self.repo = block_repo

    async def get_blocks(self) -> List[TopicBlockResponse]:
        blocks = await self.repo.find_all(['id', 'name', 'image_url'])
        result = [TopicBlockResponse.model_validate(rec) for rec in blocks]
        return result
