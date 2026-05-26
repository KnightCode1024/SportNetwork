from sport_network_api.application.dto.event import CreateEventInput, EventDTO
from sport_network_api.application.dto.user import UserDTO
from sport_network_api.application.interfaces.gateways.event_gateway import (
    EventGatewayInterface,
)
from sport_network_api.application.interfaces.uow.uow import UnitOfWorkInterface
from sport_network_api.domain.event import Event


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
            organizer=UserDTO(
                id=event.organizer.id,
                username=event.organizer.username,
                email=event.organizer.email,
                is_active=event.organizer.is_active,
                created_at=getattr(event.organizer, "created_at", None),
            ) if event.organizer else None,
            max_participants=event.max_participants,
            participants_count=event.participants_count,
            participant_ids=event.participant_ids,
            participants=[
                UserDTO(
                    id=participant.id,
                    username=participant.username,
                    email=participant.email,
                    is_active=participant.is_active,
                    created_at=getattr(participant, "created_at", None),
                )
                for participant in event.participants
            ],
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
            organizer=UserDTO(
                id=event.organizer.id,
                username=event.organizer.username,
                email=event.organizer.email,
                is_active=event.organizer.is_active,
                created_at=getattr(event.organizer, "created_at", None),
            ) if event.organizer else None,
            max_participants=event.max_participants,
            participants_count=event.participants_count,
            participant_ids=event.participant_ids,
            participants=[
                UserDTO(
                    id=participant.id,
                    username=participant.username,
                    email=participant.email,
                    is_active=participant.is_active,
                    created_at=getattr(participant, "created_at", None),
                )
                for participant in event.participants
            ],
        )


class CreateEventInteractor:
    def __init__(
        self,
        uow: UnitOfWorkInterface,
        event_gateway: EventGatewayInterface,
    ):
        self.uow = uow
        self.event_gateway = event_gateway

    async def __call__(self, organizer_id: int, event_input: CreateEventInput) -> EventDTO:
        event = Event(
            title=event_input.title,
            description=event_input.description,
            address=event_input.address,
            sport_type_id=event_input.sport_type_id,
            organizer_id=organizer_id,
            max_participants=event_input.max_participants,
        )

        async with self.uow:
            event = await self.event_gateway.create_event(event)

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
            organizer=UserDTO(
                id=event.organizer.id,
                username=event.organizer.username,
                email=event.organizer.email,
                is_active=event.organizer.is_active,
                created_at=getattr(event.organizer, "created_at", None),
            ) if event.organizer else None,
            max_participants=event.max_participants,
            participants_count=event.participants_count,
            participant_ids=event.participant_ids,
            participants=[
                UserDTO(
                    id=participant.id,
                    username=participant.username,
                    email=participant.email,
                    is_active=participant.is_active,
                    created_at=getattr(participant, "created_at", None),
                )
                for participant in event.participants
            ],
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
            organizer=UserDTO(
                id=event.organizer.id,
                username=event.organizer.username,
                email=event.organizer.email,
                is_active=event.organizer.is_active,
                created_at=getattr(event.organizer, "created_at", None),
            ) if event.organizer else None,
            max_participants=event.max_participants,
            participants_count=event.participants_count,
            participant_ids=event.participant_ids,
            participants=[
                UserDTO(
                    id=participant.id,
                    username=participant.username,
                    email=participant.email,
                    is_active=participant.is_active,
                    created_at=getattr(participant, "created_at", None),
                )
                for participant in event.participants
            ],
        )

