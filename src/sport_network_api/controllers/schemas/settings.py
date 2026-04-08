from pydantic import BaseModel, Field


class SettingsResponse(BaseModel):
    id: int
    user_id: int
    auth_2fa: bool = Field(..., description="Включена ли 2FA")
    notification_provider: str = Field(..., description="Провайдер уведомлений (EMAIL, TELEGRAM, NONE)")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "auth_2fa": False,
                "notification_provider": "EMAIL"
            }
        }


class UpdateSettingsRequest(BaseModel):
    auth_2fa: bool | None = Field(default=None, description="Включить/отключить 2FA")
    notification_provider: str | None = Field(
        default=None,
        description="Провайдер уведомлений (EMAIL, TELEGRAM, NONE)"
    )


class TwoFactorEnableResponse(BaseModel):
    secret: str = Field(..., description="Секрет для настройки 2FA")
    qr_code_uri: str = Field(..., description="URI для QR кода")
    backup_codes: list[str] = Field(..., description="Backup коды для восстановления")
    
    class Config:
        json_schema_extra = {
            "example": {
                "secret": "JBSWY3DPEHPK3PXP",
                "qr_code_uri": "otpauth://totp/SportNetwork:user@example.com?secret=JBSWY3DPEHPK3PXP&issuer=SportNetwork",
                "backup_codes": ["a1b2c3d4", "e5f6g7h8", "i9j0k1l2", "m3n4o5p6", "q7r8s9t0"]
            }
        }


class TwoFactorDisableRequest(BaseModel):
    otp_code: str = Field(..., min_length=6, max_length=6, description="6-значный OTP код")
