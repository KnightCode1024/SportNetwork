from datetime import datetime
from dishka import Provider, Scope, provide

from sport_network_api.application.interfaces.user_gateway import UserGatewayInterface
from sport_network_api.controllers.schemas.user import UserResponse


class AuthProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_current_user(self, user_gateway: UserGatewayInterface) -> UserResponse:
        return UserResponse(
            id=1,
            username="some_user",
            email="mail@mail.ru",
            is_active=True,
            created_at=datetime.now(),
        )
