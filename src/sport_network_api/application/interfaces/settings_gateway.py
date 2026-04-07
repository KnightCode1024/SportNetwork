from typing import Protocol


class SettingsGatewayInterface(Protocol):
    async def get_by_user_id(self, user_id: int) -> "SettingsDomain | None":
        ...

    async def create(self, user_id: int) -> "SettingsDomain":
        ...

    async def update(self, user_id: int, **fields) -> "SettingsDomain":
        ...

    async def delete(self, user_id: int) -> bool:
        ...
