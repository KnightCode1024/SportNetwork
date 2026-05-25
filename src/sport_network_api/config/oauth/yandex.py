from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import  HttpUrl

from sport_network_api.config.env_path import ENV_FILE


class GoogleOAuthConfig(BaseSettings):
    # model_config = SettingsConfigDict(
    #     env_file=ENV_FILE,
    #     env_prefix="GOOGLE_OAUTH_",
    #     env_file_encoding="utf-8",
    #     extra="ignore",
    # )
    #
    # CLIENT_ID: str
    # CLIENT_SECRET: str
    # REDIRECT_URL: HttpUrl
    pass
