from dataclasses import dataclass

from sport_network_api.domain.enums import NotificationProvider


@dataclass
class SettingsDTO:
    id: int
    user_id: int
    auth_2fa: bool = False
    notification_provider: NotificationProvider = NotificationProvider.EMAIL


@dataclass
class UpdateSettingsDTO:
    auth_2fa: bool = False
    notification_provider: NotificationProvider = NotificationProvider.EMAIL
