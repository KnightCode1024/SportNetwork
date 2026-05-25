from typing import Protocol

from sport_network_api.domain.event import Event


class EventGatewayInterface(Protocol):
    async def list_events(self) -> list[Event]:
        ...

    async def get_by_id(self, event_id: int) -> Event | None:
        ...

    async def register_participant(self, event_id: int, user_id: int) -> Event:
        ...
