import random
import string
import bcrypt


def generate_valid_string():
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
