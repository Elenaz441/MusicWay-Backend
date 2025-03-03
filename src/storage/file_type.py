from fastapi_storages.integrations.sqlalchemy import FileType as _FileType
from storage import my_storage
from typing import Any


class FileType(_FileType):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(storage=my_storage, *args, **kwargs)
