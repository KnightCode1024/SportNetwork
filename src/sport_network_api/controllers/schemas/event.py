from pydantic import BaseModel, Field

from sport_network_api.controllers.schemas.user import UserResponse


class EventCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    address: str = Field(..., min_length=1, max_length=255)
    sport_type_id: int = Field(...)
    max_participants: int = Field(..., gt=0)


class EventResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    address: str
    sport_type_id: int
    organizer: UserResponse
    max_participants: int
    participants_count: int
    participants: list[UserResponse] = Field(default_factory=list)
