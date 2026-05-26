from dataclasses import asdict

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException, status

from sport_network_api.application.dto.event import CreateEventInput
from sport_network_api.application.interactors.event.interactors import (
    ListEventsInteractor,
    GetEventInteractor,
    RegisterEventInteractor,
    CreateEventInteractor,
)
from sport_network_api.controllers.schemas.event import EventResponse, EventCreateRequest
from sport_network_api.controllers.schemas.user import UserResponse

router = APIRouter(
    prefix="/events",
    tags=["Events"],
    route_class=DishkaRoute,
)


@router.get("", response_model=list[EventResponse])
async def list_events(
    interactor: FromDishka[ListEventsInteractor],
) -> list[EventResponse]:
    events = await interactor()
    return [EventResponse(**asdict(event)) for event in events]


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: int,
    interactor: FromDishka[GetEventInteractor],
) -> EventResponse:
    try:
        event = await interactor(event_id)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err),
        ) from err

    return EventResponse(**asdict(event))


@router.post("", response_model=EventResponse)
async def create_event(
    event_request: EventCreateRequest,
    current_user: FromDishka[UserResponse],
    interactor: FromDishka[CreateEventInteractor],
) -> EventResponse:
    event_input = CreateEventInput(**event_request.model_dump())
    event = await interactor(current_user.id, event_input)
    return EventResponse(**asdict(event))


@router.post("/{event_id}/register", response_model=EventResponse)
async def register_event(
    event_id: int,
    current_user: FromDishka[UserResponse],
    interactor: FromDishka[RegisterEventInteractor],
) -> EventResponse:
    try:
        event = await interactor(event_id, current_user.id)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err),
        ) from err

    return EventResponse(**asdict(event))
