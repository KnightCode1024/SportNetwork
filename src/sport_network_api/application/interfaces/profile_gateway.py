from typing import Protocol

from sport_network_api.domain.user import User


class ProfileGatewayInterface(Protocol):
    async def get_by_user_id(self, user_id: int) -> User | None:
        pass
    
    async def create(self, user_id: int) -> User:
        pass

    async def update(self, user_id: int, **fields) -> User:
        pass
    
    async def delete(self, user_id: int) -> bool:
        pass
