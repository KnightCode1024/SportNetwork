from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from sport_network_api.application.interfaces import ProfileGatewayInterface
from sport_network_api.infrastructure.models.profile import Profile
from sport_network_api.domain.user import User


class ProfileGateway(ProfileGatewayInterface):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_user_id(self, user_id: int) -> User | None:
        query = select(Profile).where(Profile.user_id == user_id)
        res = await self.session.execute(query)
        model = res.scalar_one_or_none()
        return self._to_domain(model) if model else None
    
    async def create(self, user_id: int) -> User:
        pass
    
    async def update(self, user_id: int, **fields) -> User:
        pass
    
    async def delete(self, user_id: int) -> bool:
        pass
    
    def _to_domain(self, model: Profile) -> User:
        pass
