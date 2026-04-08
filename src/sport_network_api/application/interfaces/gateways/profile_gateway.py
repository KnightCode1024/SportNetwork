from typing import Protocol

from sport_network_api.domain.profile import Profile


class ProfileGatewayInterface(Protocol):
    async def get_by_user_id(self, user_id: int) -> Profile | None:
        ...

    async def create(self, profile: Profile) -> Profile:
        ...

    async def update(self, profile: Profile) -> Profile:
        ...

    async def delete(self, user_id: int) -> bool:
        ...
