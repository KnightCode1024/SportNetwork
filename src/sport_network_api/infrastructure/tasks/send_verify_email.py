from email.message import EmailMessage

import aiosmtplib

from sport_network_api.config.email import EmailConfig
from sport_network_api.config.frontend import FrontendConfig
from sport_network_api.infrastructure.taskiq_broker import broker
from sport_network_api.infrastructure.email_templates import render_template


@broker.task(task_name="send_verify_email")
async def send_verify_email(to_email: str, token: str, username: str = "") -> bool:
    email_config = EmailConfig()
    frontend_config = FrontendConfig()

    frontend_url = frontend_config.URL.rstrip("/")
    verify_link = f"{frontend_url}/verify-email/{token}"

    html_body = render_template(
        "verify_email.html",
        subject="Подтверждение email",
        username=username or "Пользователь",
        app_name="Sport Network",
        verify_link=verify_link,
    )

    message = EmailMessage()
    message["From"] = email_config.USER
    message["To"] = to_email
    message["Subject"] = "Подтверждение email — Sport Network"
    message.set_content(
        f"Здравствуйте! Для активации аккаунта перейдите по ссылке:\n\n{verify_link}\n\n"
        f"Ссылка действительна 24 часа."
    )
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
