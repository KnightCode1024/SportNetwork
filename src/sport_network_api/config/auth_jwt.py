from pathlib import Path

from pydantic_settings import BaseSettings

_certs_dir = Path("/backend/certs") if Path("/backend/certs").exists() else Path("certs")


class AuthJWTConfig(BaseSettings):
    PRIVATE_KEY: Path = _certs_dir / "jwt-private.pem"
    PUBLIC_KEY: Path = _certs_dir / "jwt-public.pem"
    ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
