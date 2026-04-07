from email.message import EmailMessage

import aiosmtplib

from sport_network_api.config.email import EmailConfig
from sport_network_api.config.frontend import FrontendConfig
from sport_network_api.infrastructure.taskiq_broker import broker
from sport_network_api.infrastructure.email_templates import render_template


@broker.task(task_name="send_reset_password_email")
async def send_reset_password_email(to_email: str, token: str, username: str = "") -> bool:
    email_config = EmailConfig()
    frontend_config = FrontendConfig()

    frontend_url = frontend_config.URL.rstrip("/")
    reset_link = f"{frontend_url}/reset-password?token={token}"

    html_body = render_template(
        "reset_password.html",
        subject="Сброс пароля",
        username=username or "Пользователь",
        app_name="Sport Network",
        reset_link=reset_link,
    )

    plain_text = (
        f"Здравствуйте, {username or 'Пользователь'}!\n\n"
        f"Мы получили запрос на сброс пароля для вашего аккаунта.\n"
        f"Перейдите по ссылке для создания нового пароля:\n\n"
        f"{reset_link}\n\n"
        f"Ссылка действительна 1 час."
    )

    message = EmailMessage()
    message["From"] = email_config.USER
    message["To"] = to_email
    message["Subject"] = "Сброс пароля — Sport Network"
    message.set_content(plain_text)
    message.add_alternative(html_body, subtype="html")

    await aiosmtplib.send(
        message,
        sender=email_config.USER,
        hostname=email_config.HOST,
        port=email_config.PORT,
        username=email_config.USER,
        password=email_config.PASSWORD,
        use_tls=email_config.USE_TLS or email_config.USE_SSL,
        timeout=60,
        tls_context=None,
    )
    return True
