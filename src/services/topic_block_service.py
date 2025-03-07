from repositories import TopicBlockRepository
from schemas import TopicBlockResponse


class TopicBlockService:
    def __init__(self, block_repo: TopicBlockRepository):
        self.block_repo = block_repo

    async def get_blocks(self) -> list[TopicBlockResponse]:
        blocks = await self.block_repo.get_topic_blocks()
        result = [TopicBlockResponse.model_validate(rec) for rec in blocks]
        return result
