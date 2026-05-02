from pydantic import BaseModel, Field, validator

from sport_network_api.domain.enums import NotificationProvider


class SettingsResponse(BaseModel):
    id: int
    user_id: int
    auth_2fa: bool = Field(..., description="Включена ли 2FA")
    notification_provider: str = Field(..., description="Провайдер уведомлений (EMAIL, TELEGRAM)")

class UpdateSettingsRequest(BaseModel):
    auth_2fa: bool | None = Field(default=None, description="Включить/отключить 2FA")
    notification_provider: NotificationProvider | None = Field(
        default=None,
        description="Провайдер уведомлений (EMAIL, TELEGRAM)"
    )

    @validator("notification_provider", pre=True)
    def normalize_notification_provider(cls, value):
        if value is None:
            return None
        if isinstance(value, NotificationProvider):
            return value
        try:
            normalized = str(value).strip().upper()
            return NotificationProvider(normalized)
        except ValueError:
            raise ValueError("notification_provider must be EMAIL or TELEGRAM")

class TwoFactorEnableResponse(BaseModel):
    secret: str = Field(..., description="Секрет для настройки 2FA")
    qr_code_uri: str = Field(..., description="URI для QR кода")
    backup_codes: list[str] = Field(..., description="Backup коды для восстановления")

class TwoFactorDisableRequest(BaseModel):
    otp_code: str = Field(..., min_length=6, max_length=6, description="6-значный OTP код")
