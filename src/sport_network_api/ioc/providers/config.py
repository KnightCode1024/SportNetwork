from dishka import Provider, Scope, provide

from sport_network_api.config.app import AppConfig
from sport_network_api.config.auth_jwt import AuthJWTConfig
from sport_network_api.config.database import DatabaseConfig
from sport_network_api.config.email import EmailConfig
from sport_network_api.config.frontend import FrontendConfig
from sport_network_api.config.rabbitmq import RabbitMQConfig
from sport_network_api.config.redis import RedisConfig
from sport_network_api.config.s3 import S3Config

class ConfigProvider(Provider):
    scope = Scope.APP

    @provide
    def get_app_config(self) -> AppConfig:
        return AppConfig()

    @provide
    def get_auth_jwt_config(self) -> AuthJWTConfig:
        return AuthJWTConfig()

    @provide
    def get_database_config(self) -> DatabaseConfig:
        return DatabaseConfig()

    @provide
    def get_email_config(self) -> EmailConfig:
        return EmailConfig()

    @provide
    def get_frontend_config(self) -> FrontendConfig:
        return FrontendConfig()

    @provide
    def get_rabbitmq_config(self) -> RabbitMQConfig:
        return RabbitMQConfig()

    @provide
    def get_redis_config(self) -> RedisConfig:
        return RedisConfig()

    @provide
    def get_s3_config(self) -> S3Config:
        return S3Config()
