from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from sport_network_api.infrastructure.gateways.user import UserGateway
from sport_network_api.infrastructure.gateways.profile import ProfileGateway
from sport_network_api.infrastructure.gateways.settings import SettingsGateway
from sport_network_api.infrastructure.gateways.token_blacklist import TokenBlacklistGateway

from sport_network_api.application.interfaces.gateways.user_gateway import UserGatewayInterface
from sport_network_api.application.interfaces.gateways.profile_gateway import ProfileGatewayInterface
from sport_network_api.application.interfaces.gateways.settings_gateway import SettingsGatewayInterface
from sport_network_api.application.interfaces.gateways.token_blacklist_gateway import TokenBlacklistGatewayInterface

from sport_network_api.config.auth_jwt import AuthJWTConfig
from sport_network_api.config.redis import RedisConfig


class GatewayProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_user_gateway(self, session: AsyncSession) -> UserGatewayInterface:
        return UserGateway(session)
    
    @provide
    def get_profile_gateway(self, session: AsyncSession) -> ProfileGatewayInterface:
        return ProfileGateway(session)
    
    @provide
    def get_settings_gateway(self, session: AsyncSession) -> SettingsGatewayInterface:
        return SettingsGateway(session)
    
    @provide(scope=Scope.APP)
    def get_token_blacklist_gateway(
        self, 
        redis_config: RedisConfig, 
        jwt_config: AuthJWTConfig,
        
    ) -> TokenBlacklistGatewayInterface:
        return TokenBlacklistGateway(redis_config, jwt_config)
