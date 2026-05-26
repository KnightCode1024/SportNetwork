from dataclasses import dataclass, field


@dataclass
class EventDTO:
    id: int | None = None
    title: str = ""
    description: str | None = None
    address: str = ""
    sport_type_id: int | None = None
    organizer_id: int | None = None
    organizer_username: str | None = None
    max_participants: int = 0
    participants_count: int = 0
    participant_ids: list[int] = field(default_factory=list)
