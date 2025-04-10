from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any


class AbstractRepository(ABC):
    @abstractmethod
    async def find_one(self, fields: List[str], **filter_by):
        """Получает одну запись, возвращая только указанные поля."""
        raise NotImplementedError

    @abstractmethod
    async def find_all(
        self,
        fields: List[str],
        filter_by: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        limit: Optional[int] = None
    ):
        """Получает все записи с поддержкой фильтрации, сортировки и ограничения количества."""
        raise NotImplementedError
