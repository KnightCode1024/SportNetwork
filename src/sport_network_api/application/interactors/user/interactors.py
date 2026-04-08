import time
from uuid import uuid4

from sport_network_api.application.dto.user import (
    RegisterUserDTO, 
    UserDTO, 
    LoginUserDTO, 
    RegisterUserInput, 
    LoginUserInput, 
    VerifyEmailInput, 
    ResetPasswordInput, 
    ResetPasswordConfirmInput, 
    LoginDeviceInfo,
    LogoutUserInput,
)
from sport_network_api.application.interfaces.gateways.user_gateway import UserGatewayInterface
from sport_network_api.application.interfaces.gateways.profile_gateway import ProfileGatewayInterface
from sport_network_api.application.interfaces.uow.uow import UnitOfWorkInterface
from sport_network_api.application.interfaces.services.password_service import PasswordServiceInterface
from sport_network_api.application.interfaces.services.jwt_service import JwtServiceInterface
from sport_network_api.application.interfaces.gateways.token_blacklist_gateway import TokenBlacklistGatewayInterface
from sport_network_api.application.interactors.user.errors import UserAlreadyExistsError

from sport_network_api.domain.user import User
from sport_network_api.domain.profile import Profile

from sport_network_api.infrastructure.tasks.send_verify_email import send_verify_email
from sport_network_api.infrastructure.tasks.send_login_notification import send_login_notification
from sport_network_api.infrastructure.tasks.send_reset_password_email import send_reset_password_email


class RegisterUserInteractor:
    def __init__(
        self,
        uow: UnitOfWorkInterface,
        user_repository: UserGatewayInterface,
        profile_repository: ProfileGatewayInterface,
        password_service: PasswordServiceInterface,
    ):
        self.uow = uow
        self.user_repository = user_repository
        self.profile_repository = profile_repository
        self.password_service = password_service

    async def __call__(self, input_data: RegisterUserInput) -> RegisterUserDTO:
        existing_user_by_email = await self.user_repository.get_by_email(input_data.email)
        if existing_user_by_email:
            raise UserAlreadyExistsError(f"Email '{input_data.email}' уже занят")
        existing_user_by_username = await self.user_repository.get_by_username(input_data.username)
        if existing_user_by_username:
            raise UserAlreadyExistsError(f"Username '{input_data.username}' уже занят")

        password_hash = self.password_service.hash_password(input_data.password)
        user = User(
            id=None,
            username=input_data.username,
            email=input_data.email,
            password_hash=password_hash,
            is_active=False,
            token=uuid4(),
        )

        async with self.uow:
            created_user = await self.user_repository.create(user)

            profile = Profile(
                user_id=created_user.id,
                date_of_birth=input_data.date_of_birth,
                gender=input_data.gender,
            )
            await self.profile_repository.create(profile)

        await send_verify_email.kiq(
            to_email=created_user.email,
            token=str(created_user.token),
            username=created_user.username,
            )

        return self._to_dto(created_user)
    
    def _to_dto(self, user: User) -> UserDTO:
        return UserDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
        )
    
class VerifyEmailInteractor:
    def __init__(
        self,
        uow: UnitOfWorkInterface,
        user_repository: UserGatewayInterface,
    ):
        self.uow = uow
        self.user_repository = user_repository

    async def __call__(self, input_data: VerifyEmailInput) -> UserDTO:
        user = await self.user_repository.get_by_token(input_data.token)
        if user is None:
            raise ValueError("Invalid or expired verification token")
        if user.is_active:
            raise ValueError("Email already verified")

        async with self.uow:
            user.activate()
            await self.user_repository.update(user)

        return self._to_dto(user)

    def _to_dto(self, user: User) -> UserDTO:
        return UserDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
        )


class LoginUserInteractor:
    def __init__(
        self,
        uow: UnitOfWorkInterface,
        user_repository: UserGatewayInterface,
        password_service: PasswordServiceInterface,
        jwt_service: JwtServiceInterface,
    ):
        self.uow = uow
        self.user_repository = user_repository
        self.password_service = password_service
        self.jwt_service = jwt_service

    async def __call__(
        self,
        input_data: LoginUserInput,
        device_info: LoginDeviceInfo,
    ) -> LoginUserDTO:
        user = await self._find_user(input_data.identifier)
        if user is None:
            raise ValueError("Invalid credentials")

        if not self.password_service.verify(input_data.password, user.password_hash):
            raise ValueError("Invalid credentials")

        device, browser = self._parse_device_info(device_info.user_agent)

        await send_login_notification.kiq(
            to_email=user.email,
            ip_address=device_info.ip_address,
            location="Unknown",
            device=device,
            browser=browser,
            username=user.username,
        )

        access_token = self.jwt_service.create_access_token(
            data={"sub": str(user.id), "email": user.email},
        )
        refresh_token = self.jwt_service.create_refresh_token(
            data={"sub": str(user.id), "email": user.email},
        )

        return LoginUserDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def _find_user(self, identifier: str) -> User | None:
        if "@" in identifier:
            return await self.user_repository.get_by_email(identifier)
        return await self.user_repository.get_by_username(identifier)

    def _parse_device_info(self, user_agent: str) -> tuple[str, str]:
        ua_lower = user_agent.lower()
        if "mobile" in ua_lower or "android" in ua_lower or "iphone" in ua_lower:
            device = "Mobile"
        elif "tablet" in ua_lower or "ipad" in ua_lower:
            device = "Tablet"
        else:
            device = "Desktop"

        if "firefox" in ua_lower:
            browser = "Firefox"
        elif "chrome" in ua_lower or "chromium" in ua_lower:
            browser = "Chrome"
        elif "safari" in ua_lower and "chrome" not in ua_lower:
            browser = "Safari"
        elif "edg" in ua_lower:
            browser = "Edge"
        else:
            browser = "Unknown"

        return device, browser


class GetUserInteractor:
    def __init__(self, user_repository: UserGatewayInterface):
        self.user_repository = user_repository

    async def __call__(self, user_id: int) -> UserDTO:
        user = await self.user_repository.get_by_id(user_id)
        if user is None:
            raise ValueError(f"User not found")
        return self._to_dto(user)

    def _to_dto(self, user: User) -> UserDTO:
        return UserDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
        )


class RequestPasswordResetInteractor:
    def __init__(
        self,
        uow: UnitOfWorkInterface,
        user_repository: UserGatewayInterface,
        password_service: PasswordServiceInterface,
    ):
        self.uow = uow
        self.user_repository = user_repository
        self.password_service = password_service

    async def __call__(self, input_data: ResetPasswordInput) -> bool:
        user = await self.user_repository.get_by_email(input_data.email)
        if user is None:
            return True

        self.password_service.generate_reset_token(user)

        async with self.uow:
            await self.user_repository.update(user)

        await send_reset_password_email.kiq(
            to_email=user.email,
            token=user.reset_token,
            username=user.username,
        )
        return True


class ConfirmPasswordResetInteractor:
    def __init__(
        self,
        uow: UnitOfWorkInterface,
        user_repository: UserGatewayInterface,
        password_service: PasswordServiceInterface,
    ):
        self.uow = uow
        self.user_repository = user_repository
        self.password_service = password_service

    async def __call__(self, input_data: ResetPasswordConfirmInput) -> bool:
        user = await self.user_repository.get_by_reset_token(input_data.token)
        if user is None:
            raise ValueError("Invalid or expired reset token")

        password_hash = self.password_service.hash_password(input_data.new_password)

        async with self.uow:
            user.password_hash = password_hash
            user.reset_token = None
            await self.user_repository.update(user)

        return True

class LogoutUserInteractor:
    def __init__(
        self,
        uow: UnitOfWorkInterface,
        user_gateway: UserGatewayInterface,
        token_blacklist_gateway: TokenBlacklistGatewayInterface,
        jwt_service: JwtServiceInterface,
    ):
        self.uow = uow
        self.user_gateway = user_gateway
        self.token_blacklist_gateway = token_blacklist_gateway
        self.jwt_service = jwt_service

    async def __call__(self, input_data: LogoutUserInput):
        try:
            access_payload = self.jwt_service.decode_jwt(input_data.access_token)
            access_exp = access_payload.get("exp", 0)
            access_ttl = max(0, int(access_exp) - int(time.time()))
            await self.token_blacklist_gateway.blacklist_token(
                input_data.access_token, access_ttl
            )
        except Exception:
            pass 

        if input_data.refresh_token:
            try:
                refresh_payload = self.jwt_service.decode_jwt(input_data.refresh_token)
                refresh_exp = refresh_payload.get("exp", 0)
                refresh_ttl = max(0, int(refresh_exp) - int(time.time()))
                await self.token_blacklist_gateway.blacklist_token(
                    input_data.refresh_token, refresh_ttl
                )
            except Exception:
                pass
