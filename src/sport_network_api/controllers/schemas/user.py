from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Имя пользователя")
    email: EmailStr = Field(..., description="Email адрес")
    password: str = Field(..., min_length=8, max_length=128, description="Пароль")
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john@example.com",
                "password": "SecurePass123!",
            }
        }


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "password": "SecurePass123!",
            }
        }


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
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "john_doe",
                "email": "john@example.com",
                "is_active": False,
                "created_at": "2026-04-01T12:00:00",
            }
        }


class RegisterResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "john_doe",
                "email": "john@example.com",
                "is_active": False,
            }
        }


class LoginResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    access_token: str
    
    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    detail: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Email 'john@example.com' уже занят",
            }
        }
