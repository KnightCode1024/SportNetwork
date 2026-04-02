from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserDTO:
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime | None = None


@dataclass
class RegisterUserDTO:
    id: int
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
