from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from sport_network_api.application.interfaces.gateways.settings_gateway import SettingsGatewayInterface
from sport_network_api.domain.enums import NotificationProvider
from sport_network_api.infrastructure.models.account_settings import AccountSetting
from sport_network_api.domain.settings import Settings


class SettingsGateway(SettingsGatewayInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_domain(self, model: AccountSetting) -> Settings:
        return Settings(
            id=model.id,
            user_id=model.user_id,
            auth_2fa=model.auth_2fa,
            notification_provider=model.notification_provider,
        )

    def _from_domain(self, settings: Settings) -> AccountSetting:
        return AccountSetting(
            user_id=settings.user_id,
            auth_2fa=settings.auth_2fa,
            notification_provider=settings.notification_provider,
        )

    async def get_by_user_id(self, user_id: int) -> Settings | None:
        query = select(AccountSetting).where(AccountSetting.user_id == user_id)
        res = await self.session.execute(query)
        model = res.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def create(self, user_id: int) -> Settings:
        settings = AccountSetting(
            user_id=user_id,
            auth_2fa=False,
            notification_provider=NotificationProvider.EMAIL,
        )
        self.session.add(settings)
        await self.session.flush()
        return self._to_domain(settings)

    async def update(self, user_id: int, **fields) -> Settings:
        orm_settings = await self._get_orm_by_user_id(user_id)
        if orm_settings is None:
            raise ValueError(f"Settings not found for user {user_id}")
        for key, value in fields.items():
            if hasattr(orm_settings, key):
                setattr(orm_settings, key, value)
        await self.session.flush()
        return self._to_domain(orm_settings)

    async def _get_orm_by_user_id(self, user_id: int) -> AccountSetting | None:
        query = select(AccountSetting).where(AccountSetting.user_id == user_id)
        res = await self.session.execute(query)
        return res.scalar_one_or_none()

    async def delete(self, user_id: int) -> bool:
        query = delete(AccountSetting).where(AccountSetting.user_id == user_id)
        res = await self.session.execute(query)
        await self.session.flush()
        return res.rowcount > 0
