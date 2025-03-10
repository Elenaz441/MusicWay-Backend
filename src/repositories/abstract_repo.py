from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Optional, Dict, Type, Any


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: Dict[str, Any]) -> UUID:
        raise NotImplementedError

    @abstractmethod
    async def edit_one(self, id: UUID, data: Dict[str, Any]) -> UUID:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id: UUID) -> UUID:
        raise NotImplementedError

    @abstractmethod
    async def find_one(
        self,
        fields: List[str],
        filter_by: Optional[Dict[str, Any]] = None
    ):
        """Получает одну запись, возвращая только указанные поля."""
        raise NotImplementedError

    @abstractmethod
    async def find_all(
        self,
        fields: List[str],
        filter_by: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        limit: Optional[int] = None,
        group_by: Optional[List[str]] = None
    ):
        """Получает все записи с поддержкой фильтрации, сортировки и ограничения количества."""
        raise NotImplementedError
