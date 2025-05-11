import random
import string
import bcrypt
import httpx
from typing import Sequence, Dict, Any, Optional
from fastapi import HTTPException, status


def generate_valid_string():
    """Генерирует строку, которая будет использоваться как пароль при первой авторизации.

    :return: Сгенерированная строка.
    """
    upper_case = string.ascii_uppercase
    digits = string.digits
    special_characters = "~!?@#$%^&*\\-_+()[]{}><\\/|\"'.:,"

    password = [
        random.choice(upper_case),
        random.choice(digits),
        random.choice(special_characters),
    ]

    remaining_chars = random.choices(
        string.ascii_letters + digits, k=7
    )

    password.extend(remaining_chars)
    random.shuffle(password)

    return ''.join(password)


def hash_password(password: str) -> str:
    """Хеширование пароля перед сохранением."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка введенного пароля с хешем из БД."""
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


async def send_query(method: str, url: str, data: Optional[Dict[str, Any]] = None) -> Any:
    """Отправка запроса на сторонний ресурс.

    :param method: Метод (POST, GET, PUT, DELETE).
    :param url: Ссылка
    :param data: Данные (если нужно).

    :return: Ответ стороннего ресурса.
    """
    async with httpx.AsyncClient() as client:
        response = await client.request(method=method, url=url, json=data, headers={'Content-Type': 'application/json'})
    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(response.content))
    return response.json()


def calculate_statistic(hw_tasks: Sequence, result: Dict[str, Any] = None) -> Dict[str, Any]:
    """Рассчитывает статистику."""
    if not result:
        result = {}
    for task in hw_tasks:
        key = task['name']
        if key not in result:
            result[key] = {'name': key, 'student_mark': 0, 'max_mark': 0}
        result[key]['student_mark'] += task['student_mark']
        result[key]['max_mark'] += task['max_mark']
    return result
