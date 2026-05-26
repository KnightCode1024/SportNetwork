from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from sport_network_api.application.interfaces.gateways.event_gateway import (
    EventGatewayInterface,
)
from sport_network_api.domain.event import Event
from sport_network_api.infrastructure.models.event import Event as EventModel
from sport_network_api.infrastructure.models.user import User as UserModel


class EventGateway(EventGatewayInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_events(self) -> list[Event]:
        query = select(EventModel).options(
            selectinload(EventModel.participants),
            selectinload(EventModel.organizer),
        )
        result = await self.session.execute(query)
        events = result.scalars().all()
        return [self._to_domain(event) for event in events]

    async def get_by_id(self, event_id: int) -> Event | None:
        query = select(EventModel).options(
            selectinload(EventModel.participants),
            selectinload(EventModel.organizer),
        ).where(EventModel.id == event_id)
        result = await self.session.execute(query)
        event_model = result.scalar_one_or_none()
        return self._to_domain(event_model) if event_model else None

    async def register_participant(self, event_id: int, user_id: int) -> Event:
        event = await self.get_event_model(event_id)
        if event is None:
            raise ValueError("Event not found")

        user_query = select(UserModel).where(UserModel.id == user_id)
        user_result = await self.session.execute(user_query)
        user_model = user_result.scalar_one_or_none()
        if user_model is None:
            raise ValueError("User not found")

        event.participants.append(user_model)
        await self.session.flush()
        await self.session.refresh(event)
        return self._to_domain(event)

    async def get_event_model(self, event_id: int) -> EventModel | None:
        query = select(EventModel).options(
            selectinload(EventModel.participants),
            selectinload(EventModel.organizer),
        ).where(EventModel.id == event_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    def _to_domain(self, event_model: EventModel) -> Event:
        return Event(
            id=event_model.id,
            title=event_model.title,
            description=event_model.description,
            address=event_model.address,
            sport_type_id=event_model.sport_type_id,
            organizer_id=event_model.organizer_id,
            organizer_username=event_model.organizer.username if event_model.organizer else None,
            max_participants=event_model.max_participants,
            participant_ids=[participant.id for participant in event_model.participants],
            participants_count=len(event_model.participants),
        )
