from pydantic import BaseModel, Field


class EventResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    address: str
    sport_type: str
    organizer_id: int
    organizer_username: str | None = None
    max_participants: int
    participants_count: int
    participants: list[int] = Field(default_factory=list)
