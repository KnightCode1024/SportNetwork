from pydantic_settings import BaseSettings, SettingsConfigDict

from sport_network_api.config.env_path import ENV_FILE


class S3Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_prefix="S3_",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    ENDPOINT: str
    PUBLIC_ENDPOINT: str
    ACCESS_KEY: str
    SECRET_KEY: str
    BUCKET_NAME: str
    REGION: str
