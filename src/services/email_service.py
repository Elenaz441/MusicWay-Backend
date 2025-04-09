from typing import Dict

from fastapi_mail import ConnectionConfig
from config import settings
from fastapi_mail import FastMail, MessageSchema, MessageType

conf = ConnectionConfig(
    MAIL_USERNAME=settings.email_sender.user,
    MAIL_PASSWORD=settings.email_sender.password,
    MAIL_PORT=settings.email_sender.port,
    MAIL_SERVER=settings.email_sender.host,

    MAIL_FROM=settings.email_sender.user,
    MAIL_FROM_NAME='MusicWay App',
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=settings.email_sender.template_folder,
)


class EmailService:
    """Сервис для отправки email-сообщений пользователям."""
    def __init__(self):
        self.fm = FastMail(conf)

    async def send_welcome_message(self, email_to: str, data: Dict[str, str]):
        """Отправляет приветственное письмо новому пользователю после регистрации.

        :param email_to: Email получателя.
        :param data: Данные для шаблона письма (например, имя пользователя)."""
        message = MessageSchema(
            subject='Регистрация в приложении MusicWay',
            recipients=[email_to],
            template_body=data,
            subtype=MessageType.html,
        )

        await self.fm.send_message(message, template_name='welcome_message.html')
