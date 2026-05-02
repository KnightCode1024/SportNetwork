from pydantic import BaseModel, EmailStr, Field, model_validator
from datetime import date, datetime

from sport_network_api.domain.enums import Gender


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Имя пользователя")
    email: EmailStr = Field(..., description="Email адрес")
    password: str = Field(..., min_length=8, max_length=128, description="Пароль")
    date_of_birth: date = Field(..., description="Дата рождения")
    gender: Gender = Field(..., description="Пол")


class LoginRequest(BaseModel):
    email: EmailStr | None = Field(default=None)
    username: str | None = Field(default=None)
    password: str = Field(..., min_length=8)

    @model_validator(mode="after")
    def check_email_or_username(self):
        if not self.email and not self.username:
            raise ValueError("Must be email or username")
        if self.email and self.username:
            raise ValueError("Must one field: email or username")
        return self

class VerifyEmailRequest(BaseModel):
    token: str = Field(..., description="Токен верификации")


class ResendVerificationRequest(BaseModel):
    email: EmailStr = Field(..., description="Email адрес")


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime | None = None
    

class RegisterResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None


class ErrorResponse(BaseModel):
    detail: str


class ResetPasswordRequest(BaseModel):
    email: EmailStr = Field(..., description="Email адрес для сброса пароля")


class ResetPasswordConfirmRequest(BaseModel):
    token: str = Field(..., description="Токен сброса пароля")
    new_password: str = Field(..., min_length=8, max_length=128, description="Новый пароль")


class ResetPasswordResponse(BaseModel):
    success: bool = Field(..., description="Успешный сброс пароля")


class RefreshRequest(BaseModel):
    refresh_token: str = Field(..., description="Refresh токен")


class OtpCode(BaseModel):
    otp_code: str = Field(..., min_length=6, max_length=6)

    @model_validator(mode="after")
    def check_otp_code(self):
        if not self.otp_code.isdigit():
            raise ValueError("Code must be digits: 123456")
        return self
