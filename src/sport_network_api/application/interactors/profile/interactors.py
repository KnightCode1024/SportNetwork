from dataclasses import dataclass
from datetime import date


@dataclass
class ProfileDTO:
    id: int
    user_id: int
    bio: str | None
    avatar_url: str | None
    date_of_birth: date | None
    gender: str | None

    @property
    def age(self) -> int | None:
        from datetime import datetime
        if self.date_of_birth is None:
            return None
        return (datetime.now().date() - self.date_of_birth).days // 365


class GetProfileInteractor:
    def __init__(self):
        pass
    
    async def __call__(self, user_id: int) -> ProfileDTO:
        pass


class UpdateProfileInteractor:
    def __init__(self):
        pass
    
    async def __call__(self, user_id: int, **fields) -> ProfileDTO:
        pass

class UploadAvatarInteractor:
    def __init__(self):
        pass
    
    async def __call__(self, user_id: int, file_bytes: bytes, filename: str) -> str:
        pass
