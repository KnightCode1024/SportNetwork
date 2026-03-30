from dishka import Provider, Scope, provide

from sport_network_api.infrastructure.gateways.user import UserGateway
from sport_network_api.application.interfaces.user_gateway import UserGatewayInterface
from sqlalchemy.ext.asyncio import AsyncSession


class GatewayProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_user_gateway(self, session: AsyncSession) -> UserGatewayInterface:
        return UserGateway(session=session)
