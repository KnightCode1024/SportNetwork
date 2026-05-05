from dataclasses import dataclass

from sport_network_api.domain.enums import NotificationProvider


@dataclass
class Settings:
    id: int | None = None
    user_id: int | None = None
    auth_2fa: bool = False
    notification_provider: NotificationProvider = NotificationProvider.EMAIL
