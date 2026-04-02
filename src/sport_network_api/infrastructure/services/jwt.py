from datetime import datetime, timedelta, UTC
from typing import TypedDict
import jwt

from sport_network_api.config.auth_jwt import AuthJWTConfig


class TokenPair(TypedDict):
    access: str
    refresh: str


class JwtService:
    def __init__(self, jwt_config: AuthJWTConfig):
        self.jwt_config = jwt_config

    def encode_jwt(
        self,
        payload: dict,
        expire_timedelta: timedelta | None = None,
        expire_minutes: int = None,
    ):
        private_key: str = self.jwt_config.PRIVATE_KEY.read_text()
        algorithm: str = self.jwt_config.ALGORITHM

        to_encode = payload.copy()
        now = datetime.now(UTC)

        if expire_timedelta:
            expire = now + expire_timedelta
        elif expire_minutes:
            expire = now + timedelta(minutes=expire_minutes)
        else:
            expire = now + timedelta(
                minutes=self.jwt_config.ACCESS_TOKEN_EXPIRE_MINUTES,
            )

        to_encode.update(
            exp=expire,
            iat=now,
        )
        encoded = jwt.encode(
            to_encode,
            private_key,
            algorithm=algorithm,
        )
        return encoded


    def decode_jwt(
        self,
        token: str | bytes,
    ):
        public_key: str = self.jwt_config.PUBLIC_KEY.read_text()
        algorithm: str = self.jwt_config.ALGORITM

        decoded = jwt.decode(
            token,
            public_key,
            algorithms=[algorithm],
        )
        return decoded


    def create_access_token(
        self,
        data: dict,
    ) -> str:
        expire_minutes: int = self.jwt_config.ACCESS_TOKEN_EXPIRE_MINUTES
        return self.encode_jwt(
            payload=data,
            expire_minutes=expire_minutes,
        )


    def create_refresh_token(self, data: dict) -> str:
        return self.encode_jwt(
            payload=data,
            expire_timedelta=timedelta(
                days=self.jwt_config.REFRESH_TOKEN_EXPIRE_DAYS,
            ),
        )