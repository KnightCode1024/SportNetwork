from pydantic_settings import BaseSettings

class OTPConfig(BaseSettings):
    TTL: int = 300
