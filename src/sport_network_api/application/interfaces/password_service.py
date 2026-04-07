from typing import Protocol

from sport_network_api.domain.user import User


class PasswordServiceInterface(Protocol):
    """Interface for password operations - application layer depends on this."""

    def hash_password(self, password: str) -> str:
        """Hash a password for storage."""
        ...

    def verify(self, password: str, password_hash: str) -> bool:
        """Verify a password against its hash."""
        ...

    def generate_reset_token(self, user: User) -> str:
        """Generate a password reset token for a user."""
        ...

    def verify_reset_token(self, user: User, token: str) -> bool:
        """Verify a password reset token."""
        ...
