import os
from collections.abc import AsyncGenerator
from unittest.mock import MagicMock

import pytest
from dishka import AsyncContainer, Provider, Scope, make_async_container, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.sport_network_api.ioc import providers
from src.sport_network_api.config.database import DatabaseConfig

@pytest.fixture(scope="session")
def postgres_config() -> DatabaseConfig:
    return DatabaseConfig(
        USER=os.getenv("DB_USER"),
        ASSWORD=os.getenv("DB_PASSWORD"),
        HOST=os.getenv("DB_HOST"),
        PORT=int(os.getenv("DB_PORT")),
        NEME=os.getenv("TEST_DB"),
    )


@pytest.fixture(scope="session")
async def session_maker(
    postgres_config: DatabaseConfig,
) -> async_sessionmaker[AsyncSession]:
    database_uri = (
        "postgresql+psycopg://{login}:{password}@{host}:{port}/{database}".format(
            login=postgres_config.login,
            password=postgres_config.password,
            host=postgres_config.host,
            port=postgres_config.port,
            database=postgres_config.database,
        )
    )
    engine = create_async_engine(database_uri)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    return async_sessionmaker(
        bind=engine, class_=AsyncSession, autoflush=False, expire_on_commit=False
    )


@pytest.fixture
async def session(
    session_maker: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession]:
    async with session_maker() as session:
        yield session
        await session.rollback()


@pytest.fixture
def container(mock_provider: Provider) -> AsyncContainer:
    return make_async_container(**providers)
