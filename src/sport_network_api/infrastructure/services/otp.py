import pyotp

from sport_network_api.config.otp import OTPConfig


class OtpService:
    def __init__(self, otp_config: OTPConfig):
        self.otp_config = otp_config

    def generate_otp_secret(self) -> str:
        return pyotp.random_base32()


    def generate_otp_code(self, otp_secret: str) -> str:
        totp = pyotp.TOTP(s=otp_secret, interval=self.otp_config.TTL)
        return totp.now()


    def verify_otp_code(self, code: str, otp_secret: str) -> bool:
        totp = pyotp.TOTP(s=otp_secret, interval=self.otp_config.TTL)
        return totp.verify(code)
    