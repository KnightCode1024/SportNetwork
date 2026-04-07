from dishka import Provider, Scope, provide

from sport_network_api.application.interactors.user.interactors import (
    RegisterUserInteractor,
    GetUserInteractor,
    LoginUserInteractor,
    VerifyEmailInteractor,
    RequestPasswordResetInteractor,
    ConfirmPasswordResetInteractor,
)
from sport_network_api.application.interfaces.user_gateway import UserGatewayInterface
from sport_network_api.application.interfaces.profile_gateway import ProfileGatewayInterface
from sport_network_api.application.interfaces.uow import UnitOfWorkInterface
from sport_network_api.application.interfaces.password_service import PasswordServiceInterface
from sport_network_api.application.interfaces.jwt_service import JwtServiceInterface


class InteractorProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_register_user_interactor(
        self,
        uow: UnitOfWorkInterface,
        user_gateway: UserGatewayInterface,
        profile_gateway: ProfileGatewayInterface,
        password_service: PasswordServiceInterface,
    ) -> RegisterUserInteractor:
        return RegisterUserInteractor(
            uow=uow,
            user_repository=user_gateway,
            profile_repository=profile_gateway,
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
