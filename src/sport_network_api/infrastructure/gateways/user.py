from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sport_network_api.domain.user import User
from sport_network_api.application.interfaces.user_gateway import UserGatewayInterface
from sport_network_api.infrastructure.models.user import User as UserModel


class UserGateway(UserGatewayInterface):    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_id(self, user_id: int) -> User | None:
        pass
    
    async def get_by_username(self, username: str) -> User | None:
        pass
    
    async def get_by_email(self, email: str) -> User | None:
        pass
    
    async def create(self, user: User) -> User:
        pass
    
    async def update(self, user: User) -> User:
        pass
    async def delete(self, user_id: int) -> bool:
        pass

    def _to_domain(self, user_model: UserModel) -> User:
        pass
    
    def _from_domain(self, user: User) -> UserModel:
        pass
