from dataclasses import dataclass


@dataclass
class SettingsDTO:
    id: int
    user_id: int
    auth_2fa: bool
    notification_provider: str
    two_factor_secret: str | None
    backup_codes: list[str] | None


class GetSettingsInteractor:    
    def __init__(self):
        pass
    
    async def __call__(self, user_id: int) -> SettingsDTO:
        pass


class UpdateSettingsInteractor:
    def __init__(self):
        pass
    
    async def __call__(self, user_id: int, **fields) -> SettingsDTO:
        pass


class Enable2faInteractor:
    def __init__(self):
        pass
    
    async def __call__(self, user_id: int) -> dict:
        pass


class Disable2faInteractor:
    def __init__(self):
        pass
    
    async def __call__(self, user_id: int, otp_code: str) -> None:
        pass
