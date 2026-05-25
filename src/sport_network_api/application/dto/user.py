from dataclasses import dataclass
from datetime import datetime, date


@dataclass
class UserDTO:
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime | None = None


@dataclass
class RegisterUserDTO:
    id: int | None 
    username: str
    email: str
    is_active: bool


@dataclass
class LoginUserDTO:
    id: int
    username: str
    email: str
    is_active: bool
    access_token: str
    refresh_token: str


@dataclass
class RegisterUserInput:
    username: str
    email: str
    password: str
    date_of_birth: date | None = None
    gender: str | None = None


@dataclass
class VerifyEmailInput:
    token: str


@dataclass
class LoginUserInput:
    email: str | None = None
    username: str | None = None
    password: str | None = None


@dataclass
class UserInput:
    id: int | None = None
    username: str | None = None
    email: str | None = None


@dataclass
class ResetPasswordInput:
    email: str


@dataclass
class ResetPasswordConfirmInput:
    token: str
    new_password: str


@dataclass
class LoginDeviceInfo:
    ip_address: str
    user_agent: str


@dataclass
class TokenPair:
    access_token: str
    refresh_token: str | None = None


@dataclass
class OtpCodeInput:
    otp_code: str


@dataclass
class RefreshTokenInput:
    refresh_token: str


@dataclass
class RefreshTokenDTO:
    id: int
    username: str
    email: str
    is_active: bool
    access_token: str
    refresh_token: str


@dataclass
class OAuthCallbackInput:
    code: str
    state: str
    redirect_uri: str


@dataclass
class OAuthUserOutput:
    id: str
    email: str
    username: str
    access_token: str
    refresh_token: str


@dataclass
class GenerateAuthUrlOutput:
    auth_url: str
    state: str
