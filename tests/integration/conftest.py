from collections.abc import AsyncIterator

import pytest
from dishka import AsyncContainer
from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka

from httpx import AsyncClient, ASGITransport

from src.sport_network_api.controllers import root_controller


@pytest.fixture
async def http_test_app(container: AsyncContainer) -> FastAPI:
    app = FastAPI()
    app.include_router(router=root_controller)
    setup_dishka(container, app)
    return app


@pytest.fixture
async def http_test_client(http_test_app: FastAPI) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=http_test_app),
        base_url="http://127.0.0.1:8001",
    ) as client:
        yield client
