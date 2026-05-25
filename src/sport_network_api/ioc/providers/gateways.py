from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from sport_network_api.infrastructure.gateways.user import UserGateway
from sport_network_api.infrastructure.gateways.profile import ProfileGateway
from sport_network_api.infrastructure.gateways.settings import SettingsGateway
from sport_network_api.infrastructure.gateways.token_blacklist import TokenBlacklistGateway
from sport_network_api.infrastructure.gateways.s3 import S3Gateway
from sport_network_api.infrastructure.gateways.event import EventGateway

from sport_network_api.application.interfaces.gateways.user_gateway import UserGatewayInterface
from sport_network_api.application.interfaces.gateways.profile_gateway import ProfileGatewayInterface
from sport_network_api.application.interfaces.gateways.settings_gateway import SettingsGatewayInterface
from sport_network_api.application.interfaces.gateways.token_blacklist_gateway import TokenBlacklistGatewayInterface
from sport_network_api.application.interfaces.gateways.s3_gateway import S3GatewayInterface
from sport_network_api.application.interfaces.gateways.event_gateway import EventGatewayInterface

from sport_network_api.config.auth_jwt import AuthJWTConfig
from sport_network_api.config.redis import RedisConfig
from sport_network_api.config.s3 import S3Config


class GatewayProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_user_gateway(self, session: AsyncSession) -> UserGatewayInterface:
        return UserGateway(session)
    
    @provide
    def get_profile_gateway(self, session: AsyncSession) -> ProfileGatewayInterface:
        return ProfileGateway(session)
    
    @provide
    def get_s3_gateway(self, s3_config: S3Config) -> S3GatewayInterface:
        return S3Gateway(
            bucket=s3_config.BUCKET_NAME,
            endpoint=s3_config.ENDPOINT,
            public_endpoint=s3_config.PUBLIC_ENDPOINT,
            access_key=s3_config.ACCESS_KEY,
            secret_key=s3_config.SECRET_KEY,
            region=s3_config.REGION,
        )

    @provide
    def get_settings_gateway(self, session: AsyncSession) -> SettingsGatewayInterface:
        return SettingsGateway(session)

    @provide
    def get_event_gateway(self, session: AsyncSession) -> EventGatewayInterface:
        return EventGateway(session)
    
    @provide(scope=Scope.APP)
    def get_token_blacklist_gateway(
        self, 
        redis_config: RedisConfig, 
        jwt_config: AuthJWTConfig,
        
    ) -> TokenBlacklistGatewayInterface:
        return TokenBlacklistGateway(redis_config, jwt_config)
