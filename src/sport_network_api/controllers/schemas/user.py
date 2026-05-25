from pydantic import BaseModel, EmailStr, Field, model_validator
from datetime import date, datetime

from sport_network_api.domain.enums import Gender


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8, max_length=128)
    date_of_birth: date = Field(...)
    gender: Gender = Field(...)


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
    token: str = Field(...)


class ResendVerificationRequest(BaseModel):
    email: EmailStr = Field(...)


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
    email: EmailStr = Field(...)


class ResetPasswordConfirmRequest(BaseModel):
    token: str = Field(...)
    new_password: str = Field(..., min_length=8, max_length=128)


class ResetPasswordResponse(BaseModel):
    success: bool = Field(...)


class RefreshRequest(BaseModel):
    refresh_token: str = Field(...)


class OtpCode(BaseModel):
    otp_code: str = Field(..., min_length=6, max_length=6)

    @model_validator(mode="after")
    def check_otp_code(self):
        if not self.otp_code.isdigit():
            raise ValueError("Code must be digits: like 123456")
        return self
