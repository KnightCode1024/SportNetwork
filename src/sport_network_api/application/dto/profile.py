from dataclasses import dataclass
from datetime import datetime, date


@dataclass
class ProfileDTO:
    id: int
    user_id: int
    bio: str | None = None
    avatar_url: str | None = None
    date_of_birth: date | None = None
    gender: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @property
    def age(self) -> int | None:
        if self.date_of_birth is None:
            return None
        return (datetime.now().date() - self.date_of_birth).days // 365


@dataclass
class ProfileWithUserDTO:
    profile: ProfileDTO
    username: str
    email: str
