from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sport_network_api.config.database import DatabaseConfig


class DatabaseProvider(Provider):
    scope = Scope.APP

    @provide(scope=Scope.APP)
    def get_session_factory(self, db_config: DatabaseConfig) -> async_sessionmaker:
        engine = create_async_engine(
            url=db_config.URL,
        )
        return async_sessionmaker(
            engine,
            expire_on_commit=False,
            autoflush=False,
        )

    @provide(scope=Scope.REQUEST)
    async def get_session(self, session_factory: async_sessionmaker) -> AsyncIterable[AsyncSession]:
        async with session_factory() as session:
            yield session

