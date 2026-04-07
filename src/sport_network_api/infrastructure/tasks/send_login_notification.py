from email.message import EmailMessage

import aiosmtplib

from sport_network_api.config.email import EmailConfig
from sport_network_api.infrastructure.taskiq_broker import broker
from sport_network_api.infrastructure.email_templates import render_template


@broker.task(task_name="send_login_notification")
async def send_login_notification(
    to_email: str,
    ip_address: str,
    location: str,
    device: str,
    browser: str,
    username: str = "",
) -> bool:
    email_config = EmailConfig()

    html_body = render_template(
        "login_notification.html",
        subject="Новый вход в аккаунт",
        username=username or "Пользователь",
        app_name="Sport Network",
        ip_address=ip_address,
        location=location,
        device=device,
        browser=browser,
    )

    plain_text = (
        f"Здравствуйте, {username or 'Пользователь'}!\n\n"
        f"Мы обнаружили вход в ваш аккаунт Sport Network с нового устройства.\n\n"
        f"Место: {location}\n"
        f"Устройство: {device}\n"
        f"Браузер: {browser}\n"
        f"IP-адрес: {ip_address}\n\n"
        f"Если это были вы — никаких действий не требуется."
    )

    message = EmailMessage()
    message["From"] = email_config.USER
    message["To"] = to_email
    message["Subject"] = "Новый вход в аккаунт — Sport Network"
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
