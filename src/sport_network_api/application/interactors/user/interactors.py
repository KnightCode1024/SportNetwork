import time
import urllib
from uuid import uuid4

from sport_network_api.application.dto.user import (
    RegisterUserDTO,
    UserDTO,
    RegisterUserInput,
    LoginUserInput,
    VerifyEmailInput,
    ResetPasswordInput,
    ResetPasswordConfirmInput,
    LoginDeviceInfo,
    RefreshTokenInput,
    RefreshTokenDTO,
    OtpCodeInput,
    TokenPair,
    UserInput,
    OAuthCallbackInput,
    OAuthUserOutput,
    GenerateAuthUrlOutput,
)
from sport_network_api.application.interfaces.gateways.token_blacklist_gateway import TokenBlacklistGatewayInterface
from sport_network_api.application.interfaces.gateways.user_gateway import UserGatewayInterface
from sport_network_api.application.interfaces.gateways.profile_gateway import ProfileGatewayInterface
from sport_network_api.application.interfaces.services.jwt_service import JwtServiceInterface
from sport_network_api.application.interfaces.services.password_service import PasswordServiceInterface
from sport_network_api.application.interfaces.services.otp_service import OtpServiceInterface
from sport_network_api.application.interfaces.uow.uow import UnitOfWorkInterface
from sport_network_api.application.interfaces.gateways.settings_gateway import SettingsGatewayInterface
from sport_network_api.application.interfaces.cache.oauth_storage import StateStorageInterface
from sport_network_api.application.interfaces.clients.google_oauth_client import GoogleOAuthClientInterface

from sport_network_api.application.interactors.user.errors import UserAlreadyExistsError

from sport_network_api.infrastructure.tasks.notification.email import (
    send_verify_email,
    send_reset_password_email,
    send_login_notification,
    send_otp_code,
)

from sport_network_api.domain.user import User
from sport_network_api.domain.profile import Profile

from sport_network_api.config.auth_jwt import AuthJWTConfig
from sport_network_api.config.frontend import FrontendConfig
from sport_network_api.config.oauth.google import GoogleOAuthConfig


class RegisterUserInteractor:
    def __init__(
        self,
        uow: UnitOfWorkInterface,
        user_repository: UserGatewayInterface,
        profile_repository: ProfileGatewayInterface,
        settings_repository: SettingsGatewayInterface,
        password_service: PasswordServiceInterface,
    ):
        self.uow = uow
        self.user_repository = user_repository
        self.profile_repository = profile_repository
        self.password_service = password_service
        self.settings_repository = settings_repository

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
            token=uuid4(),
            otp_secret=None,
        )

        async with self.uow:
            created_user = await self.user_repository.create(user)

            profile = Profile(
                user_id=created_user.id,
                date_of_birth=input_data.date_of_birth,
                gender=input_data.gender,
            )
            await self.profile_repository.create(profile)

            await self.settings_repository.create(
                user_id=created_user.id
                )

        send_verify_email.kiq(
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
        user_gateway: UserGatewayInterface,
    ):
        self.uow = uow
        self.user_gateway = user_gateway

    async def __call__(self, input_data: VerifyEmailInput) -> UserDTO:
        user = await self.user_gateway.get_by_token(input_data.token)
        if user is None:
            raise ValueError("Invalid or expired verification token")
        if user.is_active:
            raise ValueError("Email already verified")

        async with self.uow:
            user.activate()
            await self.user_gateway.update(user)

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
        user_gateway: UserGatewayInterface,
        settings_gateway: SettingsGatewayInterface,
        password_service: PasswordServiceInterface,
        jwt_service: JwtServiceInterface,
        otp_service: OtpServiceInterface,
    ):
        self.uow = uow
        self.user_gateway = user_gateway
        self.settings_gateway = settings_gateway
        self.password_service = password_service
        self.jwt_service = jwt_service
        self.otp_service = otp_service

    async def __call__(
        self,
        input_data: LoginUserInput,
        device_info: LoginDeviceInfo,
    ) -> TokenPair:
        user = await self._find_user(input_data)
        if user is None:
            print(user, type(user))
            raise ValueError("Invalid credentials")
        if not user.is_active:
            raise ValueError("Email not verified")

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

        user_settings = await self.settings_gateway.get_by_user_id(user.id)

        if not user_settings.auth_2fa or user_settings.auth_2fa is None:
            access_token = self.jwt_service.create_access_token(
                data={"sub": str(user.id), "email": user.email},
            )
            refresh_token = self.jwt_service.create_refresh_token(
                data={"sub": str(user.id), "email": user.email},
            )
            return TokenPair(
                access_token=access_token,
                refresh_token=refresh_token,
            )
        else:
            otp_secret = self.otp_service.generate_otp_secret()
            otp_code = self.otp_service.generate_otp_code(otp_secret)

            await  send_otp_code.kiq(
                user.email,
                otp_code,
            )

            async with self.uow:
                await self.user_gateway.set_otp_secret(user, otp_secret)

            access_token = self.jwt_service.create_access_token(
                data={"sub": str(user.id), "email": user.email},
                ttl=5,
            )
            return TokenPair(access_token=access_token)

    async def _find_user(self, user: LoginUserInput) -> User | None:
        if user.email is None and user.username is None:
            raise ValueError("Invalid user: not username and email")
        if user.email is not None:
            return await self.user_gateway.get_by_email(user.email)
        if user.username is not None:
            return await self.user_gateway.get_by_username(user.username)
        return None

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

        send_reset_password_email.kiq(
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

    async def __call__(self, input_data: TokenPair):
        try:
            access_payload = self.jwt_service.decode_jwt(input_data.access_token)
            access_exp = access_payload.get("exp", 0)
            access_ttl = max(0, int(access_exp) - int(time.time()))
            await self.token_blacklist_gateway.blacklist_token(
                input_data.access_token, access_ttl
            )
        except Exception as e:
            raise ValueError(str(e))

        if input_data.refresh_token:
            try:
                refresh_payload = self.jwt_service.decode_jwt(input_data.refresh_token)
                refresh_exp = refresh_payload.get("exp", 0)
                refresh_ttl = max(0, int(refresh_exp) - int(time.time()))
                await self.token_blacklist_gateway.blacklist_token(
                    input_data.refresh_token, refresh_ttl
                )
            except Exception as e:
                raise ValueError(str(e))


class RefreshTokenInteractor:
    def __init__(
        self,
        user_gateway: UserGatewayInterface,
        jwt_service: JwtServiceInterface,
    ):
        self.user_gateway = user_gateway
        self.jwt_service = jwt_service

    async def __call__(self, input_data: RefreshTokenInput) -> RefreshTokenDTO:
        try:
            decoded = self.jwt_service.decode_jwt(input_data.refresh_token)
        except Exception:
            raise ValueError("Invalid or expired refresh token")

        user_id = decoded.get("sub")
        if not user_id:
            raise ValueError("Invalid or expired refresh token")

        user = await self.user_gateway.get_by_id(int(user_id))
        if user is None or not user.is_active:
            raise ValueError("User not found or inactive")

        new_access_token = self.jwt_service.create_access_token(
            data={"sub": str(user.id), "email": user.email},
        )
        new_refresh_token = self.jwt_service.create_refresh_token(
            data={"sub": str(user.id), "email": user.email},
        )

        return RefreshTokenDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            access_token=new_access_token,
            refresh_token=new_refresh_token,
        )


class CheckCodeInteractor:
    def __init__(
        self,
        user_gateway: UserGatewayInterface,
        otp_service: OtpServiceInterface,
        jwt_service: JwtServiceInterface,
    ):
        self.user_gateway = user_gateway
        self.otp_service = otp_service
        self.jwt_service = jwt_service

    async def __call__(self, user_input: UserInput, otp_code: OtpCodeInput) -> TokenPair:
        if user_input.id:
            user = await self.user_gateway.get_by_id(user_input.id)
        elif user_input.email:
            user = await self.user_gateway.get_by_email(user_input.email)
        elif user_input.username:
            user = await self.user_gateway.get_by_username(user_input.username)
        else:
            raise ValueError("User identifier (id, email or username) is required")
        if not user:
            raise ValueError("User not found")

        otp_secret = await self.user_gateway.get_otp_secret(user)

        if not otp_secret:
            raise ValueError("OTP secret not found")
        if not self.otp_service.verify_otp_code(otp_code.otp_code, otp_secret):
            raise ValueError("Invalid code")

        return TokenPair(
            access_token=self.jwt_service.create_access_token({"sub": str(user.id), "email": user.email}),
            refresh_token=self.jwt_service.create_refresh_token({"sub": str(user.id), "email": user.email}),
        )


class ResendOtpCodeInteractor:
    def __init__(
        self,
        uow: UnitOfWorkInterface,
        user_gateway: UserGatewayInterface,
        otp_service: OtpServiceInterface,
    ):
        self.uow = uow
        self.user_gateway = user_gateway
        self.otp_service = otp_service

    async def __call__(self, input_data: LoginUserInput) -> bool:
        user = await self._find_user(input_data)
        if not user:
            raise ValueError("User not found")

        otp_secret = await self.user_gateway.get_otp_secret(user)

        if not otp_secret:
            otp_secret = self.otp_service.generate_otp_secret()
            async with self.uow:
                await self.user_gateway.set_otp_secret(user, otp_secret)

        otp_code = self.otp_service.generate_otp_code(otp_secret)

        await send_otp_code.kiq(
            to_email=user.email,
            otp_code=otp_code,
        )
        return True

    async def _find_user(self, user_input: LoginUserInput) -> User | None:
        if user_input.email:
            return await self.user_gateway.get_by_email(user_input.email)
        if user_input.username:
            return await self.user_gateway.get_by_username(user_input.username)
        return None


class HandleGoogleCallbackInteractor:
    def __init__(
        self,
        uow: UnitOfWorkInterface,
        user_gateway: UserGatewayInterface,
        profile_gateway: ProfileGatewayInterface,
        settings_gateway: SettingsGatewayInterface,
        password_service: PasswordServiceInterface,
        jwt_service: JwtServiceInterface,
        google_client: GoogleOAuthClientInterface,
        state_storage: StateStorageInterface,
    ):
        self.uow = uow
        self.user_gateway = user_gateway
        self.profile_gateway = profile_gateway
        self.settings_gateway = settings_gateway
        self.password_service = password_service
        self.jwt_service = jwt_service
        self.google_client = google_client
        self.state_storage = state_storage

    async def __call__(self, input_data: OAuthCallbackInput) -> TokenPair:
        if not await self.state_storage.consume(input_data.state):
            raise ValueError("Неверный или истёкший state")

        tokens = await self.google_client.exchange_code(
            code=input_data.code,
            redirect_uri=input_data.redirect_uri,
        )
        user_info = await self.google_client.verify_id_token(tokens["id_token"])

        email = user_info.get("email")
        if not email:
            raise ValueError("Google не вернул email")

        username = user_info.get("name") or f"google-{uuid4().hex[:12]}"
        user = await self.user_gateway.get_by_email(email)

        if user is None:
            password_hash = self.password_service.hash_password(str(uuid4()))
            user = User(
                id=None,
                username=username,
                email=email,
                password_hash=password_hash,
                token=uuid4(),
                otp_secret=None,
                is_active=True,
            )
            async with self.uow:
                user = await self.user_gateway.create(user)
                await self.profile_gateway.create(
                    Profile(user_id=user.id, date_of_birth=None, gender=None)
                )
                await self.settings_gateway.create(user_id=user.id)
        elif not user.is_active:
            async with self.uow:
                user.activate()
                await self.user_gateway.update(user)

        await send_login_notification.kiq(
            to_email=user.email,
            ip_address="OAuth",
            location="Google OAuth",
            device="Google",
            browser="OAuth",
            username=user.username,
        )

        access_token = self.jwt_service.create_access_token(
            data={"sub": str(user.id), "email": user.email},
        )
        refresh_token = self.jwt_service.create_refresh_token(
            data={"sub": str(user.id), "email": user.email},
        )

        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
        )


class GenerateOAuthGoogleUrlInteractor:
    def __init__(
        self,
        google_config: GoogleOAuthConfig,
        state_storage: StateStorageInterface,
    ):
        self.google_config = google_config
        self.state_storage = state_storage

    async def __call__(self) -> GenerateAuthUrlOutput:
        state = await self.state_storage.generate_and_store()
        redirect_uri = str(self.google_config.REDIRECT_URL)
        params = {
            "client_id": self.google_config.CLIENT_ID,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "openid profile email",
            "access_type": "offline",
            "state": state,
        }
        query_string = urllib.parse.urlencode(params)
        auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{query_string}"
        return GenerateAuthUrlOutput(auth_url=auth_url, state=state)

