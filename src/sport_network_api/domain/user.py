from uuid import UUID
from datetime import datetime

from dataclasses import dataclass, field


@dataclass
class User:
    id: int | None
    username: str
    email: str
    password_hash: str
    is_active: bool | None
    token: UUID | None
    reset_token: str | None = None
    reset_token_expires: datetime | None = None
    
    def verify_password(self, password: str) -> bool:
        import bcrypt
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())
    
    def activate(self) -> None:
        self.is_active = True
    
    def deactivate(self) -> None:
        self.is_active = False
