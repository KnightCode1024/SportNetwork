import bcrypt
import secrets
from datetime import datetime, timedelta, UTC

from sport_network_api.application.interfaces.services.password_service import PasswordServiceInterface
from sport_network_api.domain.user import User


class PasswordService(PasswordServiceInterface):
    def __init__(self, rounds: int = 12):
        self.rounds = rounds

    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt(rounds=self.rounds)
        pwd_bytes = password.encode("utf-8")
        hashed_bytes = bcrypt.hashpw(pwd_bytes, salt)
        return hashed_bytes.decode("utf-8")

    def verify(self, password: str, password_hash: str) -> bool:
        pwd_bytes = password.encode("utf-8")
        hash_bytes = password_hash.encode("utf-8")
        return bcrypt.checkpw(pwd_bytes, hash_bytes)

    def generate_reset_token(self, user: User) -> str:
        token = secrets.token_urlsafe(32)
        user.reset_token = token
        user.reset_token_expires = datetime.now(UTC) + timedelta(hours=1)
        return token

    def verify_reset_token(self, user: User, token: str) -> bool:
        if not user.reset_token or not user.reset_token_expires:
            return False
        if datetime.now(UTC) > user.reset_token_expires:
            return False
        return secrets.compare_digest(user.reset_token, token)
