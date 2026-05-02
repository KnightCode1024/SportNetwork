from typing import Protocol

from sport_network_api.domain.settings import Settings


class SettingsGatewayInterface(Protocol):
    async def get_by_user_id(self, user_id: int) -> Settings | None:
        ...

    async def create(self, user_id: int) -> Settings:
        ...

    async def update(self, user_id: int, **fields) -> Settings:
        ...

    async def delete(self, user_id: int) -> bool:
        ...
