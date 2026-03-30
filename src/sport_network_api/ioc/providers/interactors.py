from dishka import Provider, Scope, provide

from sport_network_api.application.interactors.user.interactors import RegisterUserInteractor, GetUserInteractor, LoginUserInteractor
from sport_network_api.infrastructure.gateways.user import UserGateway
from sport_network_api.application.interfaces.user_gateway import UserGatewayInterface

class InteractorProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_register_user_interactor(self, user_gateway: UserGatewayInterface) -> RegisterUserInteractor:
        return RegisterUserInteractor(user_gateway)
    
    @provide
    def get_login_user_interactor(self, user_gateway: UserGatewayInterface) -> LoginUserInteractor:
        return LoginUserInteractor(user_gateway)
    
    @provide
    def get_get_user_interactor(self, user_gateway: UserGatewayInterface) -> GetUserInteractor:
        return GetUserInteractor(UserGateway)