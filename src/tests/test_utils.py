import re
from utils import (
    generate_valid_string,
    hash_password,
    verify_password,
    calculate_statistic
)


def test_generate_valid_string():
    password = generate_valid_string()
    assert isinstance(password, str)
    assert len(password) >= 8
    assert re.search(r'[A-Z]', password)
    assert re.search(r'\d', password)
    assert re.search(r'[~!?@#$%^&*\\\-_\+\(\)\[\]{}><\\/|\"\'\.\:,]', password)


def test_password_hashing_and_verification():
    password = 'Secure123!'
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password('WrongPass', hashed)


def test_calculate_statistic():
    tasks = [
        {'name': 'Вариант 1', 'student_mark': 4, 'max_mark': 5},
        {'name': 'Вариант 1', 'student_mark': 3, 'max_mark': 5},
        {'name': 'Вариант 2', 'student_mark': 5, 'max_mark': 5},
    ]

    result = calculate_statistic(tasks)

    assert result['Вариант 1']['student_mark'] == 7
    assert result['Вариант 1']['max_mark'] == 10
    assert result['Вариант 2']['student_mark'] == 5
    assert result['Вариант 2']['max_mark'] == 5
