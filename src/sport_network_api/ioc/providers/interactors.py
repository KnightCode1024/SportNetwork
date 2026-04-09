from dishka import Provider, Scope, provide

from sport_network_api.application.interactors.user.interactors import (
    RegisterUserInteractor,
    GetUserInteractor,
    LoginUserInteractor,
    VerifyEmailInteractor,
    RequestPasswordResetInteractor,
    ConfirmPasswordResetInteractor,
    LogoutUserInteractor,
    RefreshTokenInteractor,
)
from sport_network_api.application.interfaces.gateways.user_gateway import UserGatewayInterface
from sport_network_api.application.interfaces.gateways.profile_gateway import ProfileGatewayInterface
from sport_network_api.application.interfaces.gateways.settings_gateway import SettingsGatewayInterface
from sport_network_api.application.interfaces.gateways.token_blacklist_gateway import TokenBlacklistGatewayInterface
from sport_network_api.application.interfaces.uow.uow import UnitOfWorkInterface
from sport_network_api.application.interfaces.services.password_service import PasswordServiceInterface
from sport_network_api.application.interfaces.services.jwt_service import JwtServiceInterface
from sport_network_api.application.interactors.settings.interactors import GetSettingsInteractor


class InteractorProvider(Provider):
    scope = Scope.REQUEST

    # USER MODEL
    @provide
    def get_register_user_interactor(
        self,
        uow: UnitOfWorkInterface,
        user_gateway: UserGatewayInterface,
        profile_gateway: ProfileGatewayInterface,
        settings_gateway: SettingsGatewayInterface,
        password_service: PasswordServiceInterface,
    ) -> RegisterUserInteractor:
        return RegisterUserInteractor(
            uow=uow,
            user_repository=user_gateway,
            profile_repository=profile_gateway,
            settings_repository=settings_gateway,
            password_service=password_service,
        )

    @provide
    def get_login_user_interactor(
        self,
        uow: UnitOfWorkInterface,
        user_gateway: UserGatewayInterface,
        password_service: PasswordServiceInterface,
        jwt_service: JwtServiceInterface,
    ) -> LoginUserInteractor:
        return LoginUserInteractor(
            uow=uow,
            user_repository=user_gateway,
            password_service=password_service,
            jwt_service=jwt_service,
        )

    @provide
    def get_get_user_interactor(
        self,
        user_gateway: UserGatewayInterface,
    ) -> GetUserInteractor:
        return GetUserInteractor(user_gateway)
    
    @provide
    def get_verify_email_interactor(
        self,
        uow: UnitOfWorkInterface,
        user_gateway: UserGatewayInterface,
    ) -> VerifyEmailInteractor:
        return VerifyEmailInteractor(
            uow=uow,
            user_repository=user_gateway,
        )

    @provide
    def get_request_password_reset_interactor(
        self,
        uow: UnitOfWorkInterface,
        user_gateway: UserGatewayInterface,
        password_service: PasswordServiceInterface,
    ) -> RequestPasswordResetInteractor:
        return RequestPasswordResetInteractor(
            uow=uow,
            user_repository=user_gateway,
            password_service=password_service,
        )

    @provide
    def get_confirm_password_reset_interactor(
        self,
        uow: UnitOfWorkInterface,
        user_gateway: UserGatewayInterface,
        password_service: PasswordServiceInterface,
    ) -> ConfirmPasswordResetInteractor:
        return ConfirmPasswordResetInteractor(
            uow=uow,
            user_repository=user_gateway,
            password_service=password_service,
        )

    @provide
    def get_logout_user_interactor(
        self,
        uow: UnitOfWorkInterface,
        user_gateway: UserGatewayInterface,
        token_blacklist_gateway: TokenBlacklistGatewayInterface,
        jwt_service: JwtServiceInterface,
    ) -> LogoutUserInteractor:
        return LogoutUserInteractor(
            uow=uow,
            user_gateway=user_gateway,
            token_blacklist_gateway=token_blacklist_gateway,
            jwt_service=jwt_service,
        )

    @provide
    def get_refresh_token_interactor(
        self,
        user_gateway: UserGatewayInterface,
        jwt_service: JwtServiceInterface,
    ) -> RefreshTokenInteractor:
        return RefreshTokenInteractor(
            user_repository=user_gateway,
            jwt_service=jwt_service,
        )
    
    # SETTINGS_ACCOUNT MODEL
    @provide
    def get_settings_interactor(
        self,
        settings_gateway: SettingsGatewayInterface,
    ) -> GetSettingsInteractor:
        return GetSettingsInteractor(
            settings_gateway=settings_gateway,
        )
