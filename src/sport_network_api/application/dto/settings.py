from dataclasses import dataclass

from sport_network_api.infrastructure.models.account_settings import NotificationProviderEnum


@dataclass
class SettingsDTO:
    id: int
    user_id: int
    auth_2fa: bool = False
    notification_provider: NotificationProviderEnum = NotificationProviderEnum.EMAIL
