from email.message import EmailMessage

import aiosmtplib

from sport_network_api.config.email import EmailConfig
from sport_network_api.infrastructure.taskiq_broker import broker


@broker.task(task_name="send_otp_code", retry_on_error=True, max_retries=3)
async def send_otp_code(to_email: str, otp_code: str):
    email_config = EmailConfig()
    message = EmailMessage()
    message["From"] = email_config.USER
    message["To"] = to_email
    message["Subject"] = "Verify Email"
    body = f"Ваш код для входа:\n\n{otp_code}\n\nКод действует 5 минут."
    message.set_content(body)

    await aiosmtplib.send(
        message,
        sender=email_config.USER,
        hostname=email_config.HOST,
        port=email_config.PORT,
        username=email_config.USER,
        password=email_config.PASSWORD,
        use_tls=email_config.USE_SSL,
        timeout=60,
        tls_context=None,
    )
    return True
