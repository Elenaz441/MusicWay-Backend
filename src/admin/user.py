from sqladmin import ModelView

from models import User
from utils import generate_valid_string, hash_password
from dependecies import get_email_service


class UserAdmin(ModelView, model=User):
    name = 'Пользователь'
    name_plural = 'Пользователи'
    column_list = [User.email, 'full_name', User.is_first_login, User.role]
    column_details_list = [User.email, User.surname, User.name, User.patronymic,
                           User.birthdate, User.is_first_login, User.role]
    form_columns = [User.email, User.surname, User.name, User.patronymic,
                    User.birthdate, User.role]
    column_searchable_list = [User.surname, User.name, User.patronymic, User.birthdate, User.role]
    column_labels = {
        User.email: 'Почта',
        'full_name': 'Фамилия и имя',
        User.surname: 'Фамилия',
        User.name: 'Имя',
        User.patronymic: 'Отчество',
        User.birthdate: 'Дата рождения',
        User.is_first_login: 'Первая авторизация',
        User.role: 'Роль'
    }

    async def on_model_change(self, data, model, is_created, request) -> None:
        if is_created:
            email_service = await get_email_service()
            password = generate_valid_string()
            await email_service.send_welcome_message(data['email'], {'password': password})
            print(password)
            data['hashed_password'] = hash_password(password)
