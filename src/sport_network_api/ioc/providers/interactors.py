from dishka import Provider, Scope, provide

from sport_network_api.application.interactors.user.interactors import (
    RegisterUserInteractor,
    GetUserInteractor,
    LoginUserInteractor,
)
from sport_network_api.infrastructure.gateways.user import UserGateway
from sport_network_api.application.interfaces.user_gateway import UserGatewayInterface
from sport_network_api.infrastructure.services.password import PasswordService


class InteractorProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_register_user_interactor(
        self,
        user_gateway: UserGatewayInterface,
        password_service: PasswordService,
    ) -> RegisterUserInteractor:
        return RegisterUserInteractor(
            user_repository=user_gateway,
            password_service=password_service,
        )

    @provide
    def get_login_user_interactor(
        self,
        user_gateway: UserGatewayInterface,
    ) -> LoginUserInteractor:
        return LoginUserInteractor(user_gateway)

    @provide
    def get_get_user_interactor(
        self,
        user_gateway: UserGatewayInterface,
    ) -> GetUserInteractor:
        return GetUserInteractor(user_gateway)
