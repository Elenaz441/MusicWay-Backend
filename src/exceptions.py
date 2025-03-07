class NotFoundException(Exception):
    def __init__(self, entity: str, key: str):
        self.name = f'Не найден {entity} с таким {key}'


class NoRightsException(Exception):
    def __init__(self):
        self.name = 'Нет доступа'


class InvalidTokenException(Exception):
    def __init__(self, name: str):
        self.name = name


class AlreadyExistsException(Exception):
    def __init__(self, entity: str, key: str):
        self.name = f'{entity} с таким {key} уже существует.'


class IncorrectDataException(Exception):
    def __init__(self, name: str):
        self.name = name
