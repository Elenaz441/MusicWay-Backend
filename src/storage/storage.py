from typing import BinaryIO

from fastapi_storages import S3Storage
from fastapi import HTTPException, status
from config import settings
import requests
import io
import os


class PublicAssetS3Storage(S3Storage):
    """Класс для работы с S3-хранилищем."""
    AWS_ACCESS_KEY_ID = settings.s3.key_id
    AWS_SECRET_ACCESS_KEY = settings.s3.secret
    AWS_S3_BUCKET_NAME = settings.s3.bucket_name
    AWS_S3_ENDPOINT_URL = settings.s3.endpoint_url
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_USE_SSL = True

    def open(self, name: str):
        """Открывает файл из S3 и возвращает файловый объект.

        :param name: Имя файла.

        :return: Содержание файла.

        :raises FileNotFoundError: Файл не найден.
        """

        file_url = f'https://{self.AWS_S3_ENDPOINT_URL}/{self.AWS_S3_BUCKET_NAME}/{name}'

        response = requests.get(file_url)
        if response.status_code != 200:
            raise FileNotFoundError(f'Файл {name} не найден в S3.')

        return io.BytesIO(response.content)

    def write(self, file: BinaryIO, name: str) -> str:
        """Перегружаем `write()`, чтобы проверять размер перед загрузкой."""
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)

        if file_size > 600 * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f'Файл слишком большой! (Макс. 600 MB)')

        return super().write(file, name)


my_storage = PublicAssetS3Storage()
