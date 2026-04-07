from datetime import datetime, date
from pydantic import BaseModel, Field


class ProfileResponse(BaseModel):
    id: int
    user_id: int
    bio: str | None = None
    avatar_url: str | None = None
    date_of_birth: date | None = None
    age: int | None = None
    gender: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "bio": "Люблю спорт и активный образ жизни",
                "avatar_url": "https://s3.example.com/avatars/1/avatar.jpg",
                "date_of_birth": "1990-01-01",
                "age": 36,
                "gender": "MAN",
                "created_at": "2026-01-01T00:00:00Z",
                "updated_at": "2026-01-01T00:00:00Z"
            }
        }


class UpdateProfileRequest(BaseModel):
    bio: str | None = Field(default=None, max_length=1000, description="О себе")
    date_of_birth: date | None = Field(default=None, description="Дата рождения")
    gender: str | None = Field(default=None, description="Пол (MAN, WOMEN)")


class UploadAvatarResponse(BaseModel):
    avatar_url: str = Field(..., description="URL аватарки")
    
    class Config:
        json_schema_extra = {
            "example": {
                "avatar_url": "https://s3.example.com/avatars/1/avatar_123456.jpg"
            }
        }
