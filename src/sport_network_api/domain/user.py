from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int | None
    username: str
    email: str
    password_hash: str
    is_active: bool | None
    
    def verify_password(self, password: str) -> bool:
        import bcrypt
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())
    
    def activate(self) -> None:
        self.is_active = True
    
    def deactivate(self) -> None:
        self.is_active = False
