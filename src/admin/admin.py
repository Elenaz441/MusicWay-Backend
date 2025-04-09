from sqladmin import Admin
from fastapi import FastAPI
from database import engine
from admin import (
    UserAdmin,
    MaterialAdmin,
    TopicBlockAdmin,
    FeedbackAdmin,
    LearningClassAdmin,
    StudentClassAdmin,
    AdminAuth
)


def setup_admin(app: FastAPI) -> Admin:
    """Настройка SQLAdmin с кастомной авторизацией.

    :param app: FastAPI приложение для интеграции

    :return: Экземпляр SQLAdmin для дополнительной конфигурации
    """
    auth_backend = AdminAuth()
    app.add_event_handler('startup', auth_backend.setup)
    admin = Admin(
        app,
        engine,
        authentication_backend=auth_backend
    )
    admin.add_view(UserAdmin)
    admin.add_view(MaterialAdmin)
    admin.add_view(TopicBlockAdmin)
    admin.add_view(FeedbackAdmin)
    admin.add_view(LearningClassAdmin)
    admin.add_view(StudentClassAdmin)
    return admin
