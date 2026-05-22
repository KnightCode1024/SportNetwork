from dishka import Provider, Scope, provide

from sport_network_api.infrastructure.services.password import PasswordService
from sport_network_api.infrastructure.services.jwt import JwtService
from sport_network_api.infrastructure.services.otp import OtpService
from sport_network_api.infrastructure.services.s3 import S3Service

from sport_network_api.application.interfaces.services.password_service import PasswordServiceInterface
from sport_network_api.application.interfaces.services.jwt_service import JwtServiceInterface
from sport_network_api.application.interfaces.services.otp_service import OtpServiceInterface
from sport_network_api.application.interfaces.services.s3_service import S3ServiceInterface

from sport_network_api.config.auth_jwt import AuthJWTConfig
from sport_network_api.config.otp import OTPConfig
from sport_network_api.config.s3 import S3Config


class ServiceProvider(Provider):
    scope = Scope.APP

    @provide
    def get_password_service(self) -> PasswordServiceInterface:
        return PasswordService()

    @provide
    def get_jwt_service(self, jwt_config: AuthJWTConfig) -> JwtServiceInterface:
        return JwtService(jwt_config=jwt_config)

    @provide
    def get_otp_service(self, otp_config: OTPConfig) -> OtpServiceInterface:
        return OtpService(otp_config)

    @provide
    def get_s3_service(self, s3_config: S3Config) -> S3ServiceInterface:
        return S3Service(
            bucket=s3_config.BUCKET_NAME,
            endpoint=s3_config.ENDPOINT,
            public_endpoint=s3_config.PUBLIC_ENDPOINT,
            access_key=s3_config.ACCESS_KEY,
            secret_key=s3_config.SECRET_KEY,
            region=s3_config.REGION,
        )
