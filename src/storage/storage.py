from fastapi_storages import FileSystemStorage
from config import BASE_DIR

my_storage = FileSystemStorage(path=f'{BASE_DIR}/files')
