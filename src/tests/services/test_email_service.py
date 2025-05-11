import pytest
from unittest.mock import AsyncMock, patch
from services.email_service import EmailService


@pytest.mark.asyncio
@patch("services.email_service.FastMail")
async def test_send_welcome_message(mock_fastmail_class):
    mock_fastmail = AsyncMock()
    mock_fastmail_class.return_value = mock_fastmail

    service = EmailService()
    email_to = 'test@example.com'
    data = {'username': 'Тест'}

    await service.send_welcome_message(email_to, data)

    mock_fastmail.send_message.assert_called_once()
    args, kwargs = mock_fastmail.send_message.call_args

    message = args[0]
    assert message.subject == 'Регистрация в приложении MusicWay'
    assert message.recipients == [email_to]
    assert message.template_body == data
    assert kwargs['template_name'] == 'welcome_message.html'
