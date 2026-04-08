from dishka import Provider, Scope, provide

from sport_network_api.infrastructure.services.password import PasswordService
from sport_network_api.infrastructure.services.jwt import JwtService
from sport_network_api.application.interfaces.services.password_service import PasswordServiceInterface
from sport_network_api.application.interfaces.services.jwt_service import JwtServiceInterface
from sport_network_api.config.auth_jwt import AuthJWTConfig


class ServiceProvider(Provider):
    scope = Scope.APP

    @provide
    def get_password_service(self) -> PasswordServiceInterface:
        return PasswordService(rounds=12)

    @provide
    def get_jwt_service(self, jwt_config: AuthJWTConfig) -> JwtServiceInterface:
        return JwtService(jwt_config=jwt_config)
