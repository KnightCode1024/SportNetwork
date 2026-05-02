from uuid import UUID
from datetime import datetime

from dataclasses import dataclass, field


@dataclass
class User:
    id: int | None
    username: str
    email: str
    password_hash: str
    token: UUID | None
    otp_secret: str | None
    is_active: bool | None = False
    
    def activate(self) -> None:
        self.is_active = True
