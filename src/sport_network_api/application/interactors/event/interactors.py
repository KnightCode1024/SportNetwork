from sport_network_api.application.dto.event import EventDTO
from sport_network_api.application.interfaces.gateways.event_gateway import (
    EventGatewayInterface,
)
from sport_network_api.application.interfaces.uow.uow import UnitOfWorkInterface


class ListEventsInteractor:
    def __init__(self, event_gateway: EventGatewayInterface):
        self.event_gateway = event_gateway

    async def __call__(self) -> list[EventDTO]:
        events = await self.event_gateway.list_events()
        return [self._to_dto(event) for event in events]

    def _to_dto(self, event) -> EventDTO:
        return EventDTO(
            id=event.id,
            title=event.title,
            description=event.description,
            address=event.address,
            sport_type_id=event.sport_type_id,
            organizer_id=event.organizer_id,
            organizer_username=event.organizer_username,
            max_participants=event.max_participants,
            participants_count=event.participants_count,
            participant_ids=event.participant_ids,
        )


class GetEventInteractor:
    def __init__(self, event_gateway: EventGatewayInterface):
        self.event_gateway = event_gateway

    async def __call__(self, event_id: int) -> EventDTO:
        event = await self.event_gateway.get_by_id(event_id)
        if event is None:
            raise ValueError("Event not found")
        return self._to_dto(event)

    def _to_dto(self, event) -> EventDTO:
        return EventDTO(
            id=event.id,
            title=event.title,
            description=event.description,
            address=event.address,
            sport_type_id=event.sport_type_id,
            organizer_id=event.organizer_id,
            organizer_username=event.organizer_username,
            max_participants=event.max_participants,
            participants_count=event.participants_count,
            participant_ids=event.participant_ids,
        )


class RegisterEventInteractor:
    def __init__(
        self,
        uow: UnitOfWorkInterface,
        event_gateway: EventGatewayInterface,
    ):
        self.uow = uow
        self.event_gateway = event_gateway

    async def __call__(self, event_id: int, user_id: int) -> EventDTO:
        event = await self.event_gateway.get_by_id(event_id)
        if event is None:
            raise ValueError("Event not found")

        if user_id in event.participant_ids:
            raise ValueError("User already registered for the event")

        if event.participants_count >= event.max_participants:
            raise ValueError("Event is full")

        async with self.uow:
            event = await self.event_gateway.register_participant(event_id, user_id)

        return self._to_dto(event)

    def _to_dto(self, event) -> EventDTO:
        return EventDTO(
            id=event.id,
            title=event.title,
            description=event.description,
            address=event.address,
            sport_type_id=event.sport_type_id,
            organizer_id=event.organizer_id,
            organizer_username=event.organizer_username,
            max_participants=event.max_participants,
            participants_count=event.participants_count,
            participant_ids=event.participant_ids,
        )

