from sqladmin import ModelView
from sqlalchemy import Select, select
from sqlalchemy.orm import join
from starlette.requests import Request

from models import User, Role


class UserAdmin(ModelView, model=User):
    name = 'Пользователь'
    name_plural = 'Пользователи'
    column_list = [User.email, 'full_name', User.is_first_login, User.role]
    column_details_list = [User.email, User.surname, User.name, User.patronymic,
                           User.birthdate, User.is_first_login, User.role]
    form_columns = [User.email, User.surname, User.name, User.patronymic,
                    User.birthdate, User.role, User.hashed_password]
    column_searchable_list = [User.surname, User.name, User.patronymic, User.birthdate, User.role]
    column_labels = {
        User.email: 'Почта',
        'full_name': 'Фамилия и имя',
        User.surname: 'Фамилия',
        User.name: 'Имя',
        User.patronymic: 'Отчество',
        User.birthdate: 'Дата рождения',
        User.is_first_login: 'Первая регистрация',
        User.role: 'Роль'
    }

    # def list_query(self, request: Request) -> Select:
    #     return select(User).join(Role, User.role_id == Role.id)

#  select(User)
#  .select_from(join(User, Address, User.addresses))
#  .filter(Address.email_address == "foo@bar.com")

# select(Order.id, Order.product, Customer.name).select_from(
#     Order).join(Customer, Order.customer_id == Customer.id)

