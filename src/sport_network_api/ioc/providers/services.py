from dishka import Provider, Scope, provide

from sport_network_api.infrastructure.services.password import PasswordService


class ServiceProvider(Provider):
    """Провайдер для сервисов (Scope.APP - создаются один раз)"""
    scope = Scope.APP

    @provide
    def get_password_service(self) -> PasswordService:
        """Создать PasswordService"""
        return PasswordService(rounds=12)
