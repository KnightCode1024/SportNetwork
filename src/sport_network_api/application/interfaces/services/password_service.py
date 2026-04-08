from typing import Protocol

from sport_network_api.domain.user import User


class PasswordServiceInterface(Protocol):
    def hash_password(self, password: str) -> str:
        ...

    def verify(self, password: str, password_hash: str) -> bool:
        ...

    def generate_reset_token(self, user: User) -> str:
        ...

    def verify_reset_token(self, user: User, token: str) -> bool:
        ...
