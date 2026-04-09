from sport_network_api.application.dto.settings import SettingsDTO
from sport_network_api.application.interfaces.gateways.settings_gateway import SettingsGatewayInterface


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
        return self._to_domain(settings)

    def _to_domain(self, model) -> SettingsDTO:
        return SettingsDTO(
            id=model.id,
            user_id=model.user_id,
            auth_2fa=model.auth_2fa,
            notification_provider=model.notification_provider.value,
        )
