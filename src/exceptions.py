class NotFoundException(Exception):
    def __init__(self, entity: str, key: str):
        self.name = f'Не найден {entity} с таким {key}'