from sport_network_api.application.dto.settings import SettingsDTO, UpdateSettingsDTO
from sport_network_api.application.interfaces.gateways.settings_gateway import SettingsGatewayInterface
from sport_network_api.application.interfaces.uow.uow import UnitOfWorkInterface


class GetSettingsInteractor:
    def __init__(
        self,
        settings_gateway: SettingsGatewayInterface,
    ):
        self.settings_gateway = settings_gateway

    async def __call__(self, user_id: int) -> SettingsDTO:
        settings = await self.settings_gateway.get_by_user_id(user_id)
        if settings is None:
            raise ValueError("Settings not found")
        return self._to_dto(settings)

    def _to_dto(self, settings) -> SettingsDTO:
        return SettingsDTO(
            id=settings.id,
            user_id=settings.user_id,
            auth_2fa=settings.auth_2fa,
            notification_provider=settings.notification_provider,
        )

class UpdateSettingsInteractor:
    def __init__(
            self,
            uow: UnitOfWorkInterface,
            settings_gateway: SettingsGatewayInterface,
    ):
        self.settings_gateway = settings_gateway
        self.uow = uow

    async def __call__(self, user_id: int, settings_data: UpdateSettingsDTO) -> SettingsDTO:
        async with self.uow:
            update_fields = {}
            if settings_data.auth_2fa is not None:
                update_fields["auth_2fa"] = settings_data.auth_2fa
            if settings_data.notification_provider is not None:
                update_fields["notification_provider"] = settings_data.notification_provider
            user_settings = await self.settings_gateway.update(user_id, **update_fields)
            return self._to_dto(user_settings)

    def _to_dto(self, settings) -> SettingsDTO:
        return SettingsDTO(
            id=settings.id,
            user_id=settings.user_id,
            auth_2fa=settings.auth_2fa,
            notification_provider=settings.notification_provider,
        )