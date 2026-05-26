from dataclasses import dataclass, field

from sport_network_api.application.dto.user import UserDTO


@dataclass
class CreateEventInput:
    title: str
    address: str
    sport_type_id: int
    description: str | None = None
    max_participants: int = 1


@dataclass
class EventDTO:
    id: int | None = None
    title: str = ""
    description: str | None = None
    address: str = ""
    sport_type_id: int | None = None
    organizer_id: int | None = None
    organizer_username: str | None = None
    organizer: UserDTO | None = None
    max_participants: int = 0
    participants_count: int = 0
    participant_ids: list[int] = field(default_factory=list)
    participants: list[UserDTO] = field(default_factory=list)
