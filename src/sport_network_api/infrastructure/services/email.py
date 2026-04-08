from email.message import EmailMessage

import aiosmtplib

from sport_network_api.config.email import EmailConfig
from sport_network_api.config.frontend import FrontendConfig


class EmailService:
    def __init__(self, email_config: EmailConfig, frontend_config: FrontendConfig):
        self.email_config = email_config
        self.frontend_config = frontend_config
    
    async def send_email(self, to_email: str, subject: str, body: str) -> bool:
        msg = EmailMessage()
        msg["From"] = self.email_config.USER
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)

        try:
            await aiosmtplib.send(
                msg,
                sender=self.email_config.USER,
                hostname=self.email_config.HOST,
                port=self.email_config.PORT,
                username=self.email_config.USER,
                password=self.email_config.PASSWORD,
                use_tls=self.email_config.USE_TLS,
                timeout=60,
                tls_context=None,
            )
            return True
        except Exception as e:
            print(str(e))
            return False
    
    async def send_welcome_email(self, to_email: str, username: str) -> bool:
        subject = "Welcome Email"
        body = f"""
        Привет, {username}!\n\n
        Добро пожаловать в наш сервис!
        """
        success = await self.send_email(to_email=to_email, subject=subject, body=body)
        return success
    
    async def send_2fa_code(self, to_email: str, code: str) -> bool:
        subject = "2FA code"
        body = f"""
        Ваш код: {code}\n\n
        Код действует 5 минут0
        """
        success = await self.send_email(to_email=to_email, subject=subject, body=body)
        return success
    
    async def send_password_reset(self, to_email: str, token: str) -> bool:
        subject = "Reset Password"
        link = f"{self.frontend_config.URL}/users/reset-password?token={token}"
        body = f"""
        Перейдите по ссылке для сброса пароля:\n\n
        {link}
        """
        success = await self.send_email(to_email=to_email, subject=subject, body=body)
        return success
    
    async def send_login_notification(
        self,
        to_email: str,
        ip_address: str,
        location: str,
        device: str,
    ) -> bool:
        subject = "Login notification"
        body = f"""
        В ваш аккаунт вошли.\n\n
        IP: {ip_address}\n
        Место: {location}
        Устройство: {device}
        """
        success = await self.send_email(to_email=to_email, subject=subject, body=body)
        return success
