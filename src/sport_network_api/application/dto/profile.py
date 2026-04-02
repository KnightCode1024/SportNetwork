from dataclasses import dataclass
from datetime import datetime


@dataclass
class ProfileDTO:
    id: int
    user_id: int
    bio: str | None = None
    avatar_url: str | None = None
    age: int | None = None
    gender: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class ProfileWithUserDTO:
    profile: ProfileDTO
    username: str
    email: str
