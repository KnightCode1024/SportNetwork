from pydantic_settings import BaseSettings, SettingsConfigDict


from sport_network_api.config.env_path import ENV_FILE

class EmailConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_prefix="EMAIL_",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    USE_TLS: bool
