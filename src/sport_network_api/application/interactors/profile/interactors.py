from dataclasses import dataclass


@dataclass
class ProfileDTO:
    id: int
    user_id: int
    bio: str | None
    avatar_url: str | None
    age: int | None
    gender: str | None


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
