from pydantic_settings import BaseSettings, SettingsConfigDict

from sport_network_api.config.env_path import ENV_FILE


class APPConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_prefix="APP_",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    NAME: str
    MODE: str = "dev"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    SECRET_KEY: str
