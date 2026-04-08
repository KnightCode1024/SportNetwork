from pydantic_settings import BaseSettings, SettingsConfigDict

from sport_network_api.config.env_path import ENV_FILE


class RabbitMQConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_prefix="RABBITMQ_",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    HOST: str
    PORT: int
    USER: str
    PASSWORD: str

    @property
    def URL(self):
        return f"amqp://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}//"
    