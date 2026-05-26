from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from sport_network_api.domain.user import User


@dataclass
class Event:
    id: int | None = None
    title: str = ""
    description: str | None = None
    address: str = ""
    sport_type_id: int | None = None
    organizer_id: int | None = None
    organizer_username: str | None = None
    organizer: User | None = None
    max_participants: int = 0
    participant_ids: list[int] = field(default_factory=list)
    participants: list[User] = field(default_factory=list)
    participants_count: int = 0
