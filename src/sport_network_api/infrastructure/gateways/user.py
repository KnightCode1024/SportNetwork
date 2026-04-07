from uuid import UUID
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from sport_network_api.domain.user import User
from sport_network_api.application.interfaces.user_gateway import UserGatewayInterface
from sport_network_api.application.interfaces.uow import UnitOfWorkInterface
from sport_network_api.infrastructure.models.user import User as UserModel


class UserGateway(UserGatewayInterface):
    def __init__(self, session: AsyncSession):
        self.session= session

    async def get_by_id(self, user_id: int) -> User | None:
        query = select(UserModel).where(UserModel.id == user_id)
        res = await self.session.execute(query)
        user_model = res.scalar_one_or_none()
        return self._to_domain(user_model) if user_model else None

    async def get_by_username(self, username: str) -> User | None:
        query = select(UserModel).where(UserModel.username == username)
        res = await self.session.execute(query)
        user_model = res.scalar_one_or_none()
        return self._to_domain(user_model) if user_model else None

    async def get_by_email(self, email: str) -> User | None:
        query = select(UserModel).where(UserModel.email == email)
        res = await self.session.execute(query)
        user_model = res.scalar_one_or_none()
        return self._to_domain(user_model) if user_model else None

    async def get_by_token(self, token: str) -> User | None:
        try:
            token_uuid = UUID(token)
        except ValueError:
            return None
        query = select(UserModel).where(UserModel.token == token_uuid)
        res = await self.session.execute(query)
        user_model = res.scalar_one_or_none()
        return self._to_domain(user_model) if user_model else None

    async def get_by_reset_token(self, token: str) -> User | None:
        from datetime import datetime, UTC
        now = datetime.now(UTC)
        query = select(UserModel).where(
            UserModel.reset_token == token,
            UserModel.reset_token_expires > now,
        )
        res = await self.session.execute(query)
        user_model = res.scalar_one_or_none()
        return self._to_domain(user_model) if user_model else None

    async def create(self, user: User) -> User:
        user_model = self._from_domain(user)
        self.session.add(user_model)
        await self.session.flush()
        return self._to_domain(user_model)

    async def update(self, user: User) -> User:
        query = select(UserModel).where(UserModel.id == user.id)
        res = await self.session.execute(query)
        user_model = res.scalar_one()

        user_model.username = user.username
        user_model.email = user.email
        user_model.password = user.password_hash
        user_model.is_active = user.is_active
        user_model.token = user.token
        user_model.reset_token = user.reset_token
        user_model.reset_token_expires = user.reset_token_expires

        await self.session.flush()
        await self.session.refresh(user_model)
        return self._to_domain(user_model)

    async def delete(self, user_id: int) -> bool:
        query = delete(UserModel).where(UserModel.id == user_id)
        res = await self.session.execute(query)
        await self.session.flush()
        return res.rowcount > 0

    def _to_domain(self, user_model: UserModel) -> User:
        return User(
            id=user_model.id,
            username=user_model.username,
            email=user_model.email,
            password_hash=user_model.password,
            is_active=user_model.is_active,
            token=user_model.token,
            reset_token=user_model.reset_token,
            reset_token_expires=user_model.reset_token_expires,
        )

    def _from_domain(self, user: User) -> UserModel:
        return UserModel(
            username=user.username,
            email=user.email,
            password=user.password_hash,
            is_active=user.is_active,
            token=user.token,
            reset_token=user.reset_token,
            reset_token_expires=user.reset_token_expires,
        )
