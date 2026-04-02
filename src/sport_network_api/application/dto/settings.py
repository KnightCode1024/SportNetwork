from dataclasses import dataclass
from typing import Optional


@dataclass
class SettingsDTO:
    id: int
    user_id: int
    auth_2fa: bool = False
    notification_provider: str = "EMAIL"
    two_factor_secret: Optional[str] = None
    backup_codes: Optional[list[str]] = None
