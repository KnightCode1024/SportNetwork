from dataclasses import dataclass
from enum import Enum

from sport_network_api.domain.enums import NotificationProvider


@dataclass
class Settings:
    id: int | None = None
    user_id: int | None = None
    auth_2fa: bool = False
    notification_provider: NotificationProvider = NotificationProvider.EMAIL

    def enable_2fa(self) -> None:
        self.auth_2fa = True

    def disable_2fa(self) -> None:
        self.auth_2fa = False

    def set_notification_provider(self, provider: NotificationProvider) -> None:
        self.notification_provider = provider
