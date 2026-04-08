from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime

from sport_network_api.infrastructure.models.profile import GenderEnum


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Имя пользователя")
    email: EmailStr = Field(..., description="Email адрес")
    password: str = Field(..., min_length=8, max_length=128, description="Пароль")
    date_of_birth: date = Field(..., description="Дата рождения")
    gender: GenderEnum = Field(..., description="Пол")


class LoginRequest(BaseModel):
    identifier: str = Field(..., description="Имя пользователя или email")
    password: str = Field(..., min_length=8)

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
    refresh_token: str


class ErrorResponse(BaseModel):
    detail: str


class ResetPasswordRequest(BaseModel):
    email: EmailStr = Field(..., description="Email адрес для сброса пароля")


class ResetPasswordConfirmRequest(BaseModel):
    token: str = Field(..., description="Токен сброса пароля")
    new_password: str = Field(..., min_length=8, max_length=128, description="Новый пароль")


class ResetPasswordResponse(BaseModel):
    success: bool = Field(..., description="Успешный сброс пароля")
