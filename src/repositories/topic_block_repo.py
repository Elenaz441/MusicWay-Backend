from models import TopicBlock
from .sqlalchemy_repo import SQLAlchemyRepository


class TopicBlockRepository(SQLAlchemyRepository):
    """Репозиторий для разделов (тематических блоков)."""
    model = TopicBlock
