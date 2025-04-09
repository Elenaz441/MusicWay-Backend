from fastapi_storages.integrations.sqlalchemy import FileType as _FileType
from fastapi_storages.base import StorageFile
from storage import my_storage
from typing import Any


class FileType(_FileType):
    """Специальный тип для работы с файлами."""
    def __init__(self, model_name, *args: Any, **kwargs: Any) -> None:
        super().__init__(storage=my_storage, *args, **kwargs)
        self.model_name = model_name

    def process_bind_param(self, value, dialect):
        """Добавляем префикс (название таблицы) перед сохранением в БД.

        :param value: Первоначальное имя файла.
        :param dialect:

        :return: Имя файла.
        """
        if value is None:
            return value
        if len(value.file.read(1)) != 1:
            return None
        if self.model_name:
            value.filename = f'{self.model_name}-{value.filename}'

        file = StorageFile(name=value.filename, storage=self.storage)
        file.write(file=value.file)

        value.file.close()
        return file.name
