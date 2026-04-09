from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from sport_network_api.application.interfaces.gateways.settings_gateway import SettingsGatewayInterface
from sport_network_api.infrastructure.models.account_settings import AccountSetting, NotificationProviderEnum


class SettingsGateway(SettingsGatewayInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_user_id(self, user_id: int) -> AccountSetting | None:
        query = select(AccountSetting).where(AccountSetting.user_id == user_id)
        res = await self.session.execute(query)
        return res.scalar_one_or_none()

    async def create(self, user_id: int) -> AccountSetting:
        settings = AccountSetting(
            user_id=user_id,
            auth_2fa=False,
            notification_provider=NotificationProviderEnum.EMAIL,
        )
        self.session.add(settings)
        await self.session.flush()
        return settings

    async def update(self, user_id: int, **fields) -> AccountSetting:
        settings = await self.get_by_user_id(user_id)
        if settings is None:
            raise ValueError(f"Settings not found for user {user_id}")
        for key, value in fields.items():
            if hasattr(settings, key):
                setattr(settings, key, value)
        await self.session.flush()
        return settings

    async def delete(self, user_id: int) -> bool:
        query = delete(AccountSetting).where(AccountSetting.user_id == user_id)
        res = await self.session.execute(query)
        await self.session.flush()
        return res.rowcount > 0
