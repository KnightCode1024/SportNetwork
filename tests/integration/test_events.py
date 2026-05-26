import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.sport_network_api.infrastructure.models import Event as EventModel


@pytest.mark.asyncio
async def test_create_event_and_get_event(
    http_client: AsyncClient,
    session: AsyncSession,
    create_user,
    create_sport_type,
    access_token_factory,
) -> None:
    organizer = await create_user("organizer", "organizer@example.com")
    sport_type = await create_sport_type("Football")
    await session.commit()

    token = access_token_factory(organizer.id)
    payload = {
        "title": "Sunday Match",
        "description": "Friendly game",
        "address": "Central Park",
        "sport_type_id": sport_type.id,
        "max_participants": 4,
    }

    response = await http_client.post(
        "/api/v1/events",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    event_data = response.json()
    assert event_data["title"] == payload["title"]
    assert event_data["address"] == payload["address"]
    assert event_data["organizer"]["id"] == organizer.id
    assert event_data["organizer"]["username"] == organizer.username
    assert event_data["participants"] == []
    assert event_data["max_participants"] == 4

    event_id = event_data["id"]
    get_response = await http_client.get(f"/api/v1/events/{event_id}")
    assert get_response.status_code == status.HTTP_200_OK
    loaded_event = get_response.json()
    assert loaded_event["id"] == event_id
    assert loaded_event["organizer"]["email"] == organizer.email
    assert loaded_event["participants"] == []


@pytest.mark.asyncio
async def test_list_events_returns_events_with_organizer(
    http_client: AsyncClient,
    session: AsyncSession,
    create_user,
    create_sport_type,
) -> None:
    user = await create_user("list_user", "list_user@example.com")
    sport_type = await create_sport_type("Basketball")
    event = EventModel(
        title="Weekend Game",
        description="Open court",
        address="Town Hall",
        sport_type_id=sport_type.id,
        organizer_id=user.id,
        max_participants=10,
    )
    session.add(event)
    await session.commit()

    response = await http_client.get("/api/v1/events")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()
    assert any(item["id"] == event.id for item in items)

    returned_event = next(item for item in items if item["id"] == event.id)
    assert returned_event["organizer"]["id"] == user.id
    assert returned_event["participants"] == []


@pytest.mark.asyncio
async def test_register_event_adds_participant_and_blocks_duplicate(
    http_client: AsyncClient,
    session: AsyncSession,
    create_user,
    create_sport_type,
    access_token_factory,
) -> None:
    organizer = await create_user("organizer_two", "organizer_two@example.com")
    participant = await create_user("participant", "participant@example.com")
    sport_type = await create_sport_type("Volleyball")
    event = EventModel(
        title="Beach Practice",
        description="Prepare for tournament",
        address="Seaside Arena",
        sport_type_id=sport_type.id,
        organizer_id=organizer.id,
        max_participants=2,
    )
    session.add(event)
    await session.commit()

    token = access_token_factory(participant.id)
    register_response = await http_client.post(
        f"/api/v1/events/{event.id}/register",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert register_response.status_code == status.HTTP_200_OK
    data = register_response.json()
    assert data["participants_count"] == 1
    assert len(data["participants"]) == 1
    assert data["participants"][0]["id"] == participant.id

    duplicate_response = await http_client.post(
        f"/api/v1/events/{event.id}/register",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert duplicate_response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already registered" in duplicate_response.json()["detail"]
