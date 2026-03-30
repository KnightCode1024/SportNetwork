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
    user: UserDTO
    access_token: str


@dataclass
class LoginUserDTO:
    user: UserDTO
    access_token: str
