from dishka import Provider, Scope, provide

from sport_network_api.infrastructure.gateways.user import UserGateway
from sport_network_api.infrastructure.gateways.profile import ProfileGateway
from sport_network_api.infrastructure.gateways.settings import SettingsGateway
from sport_network_api.application.interfaces.user_gateway import UserGatewayInterface
from sport_network_api.application.interfaces.profile_gateway import ProfileGatewayInterface
from sport_network_api.application.interfaces.settings_gateway import SettingsGatewayInterface
from sport_network_api.application.interfaces.uow import UnitOfWorkInterface


from sqlalchemy.ext.asyncio import AsyncSession

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
