from redis.asyncio import Redis, from_url

from sport_network_api.application.interfaces.gateways.token_blacklist_gateway import TokenBlacklistGatewayInterface
from sport_network_api.config.redis import RedisConfig
from sport_network_api.config.auth_jwt import AuthJWTConfig


class TokenBlacklistGateway(TokenBlacklistGatewayInterface):
    def __init__(
            self, 
            redis_config: RedisConfig, 
            jwt_config: AuthJWTConfig,
        ):
        self.redis_config = redis_config
        self.jwt_config = jwt_config
        self._redis: Redis | None = None

    async def _get_redis(self) -> Redis:
        if self._redis is None:
            self._redis = from_url(
                f"redis://{self.redis_config.HOST}:{self.redis_config.PORT}",
                encoding="utf-8",
                decode_responses=True,
            )
        return self._redis

    async def blacklist_token(self, token: str, ttl: int) -> None:
        r = await self._get_redis()
        try:
            await r.setex(f"blacklist:{token}", ttl, "1")
        except Exception:
            pass

    async def is_blacklisted(self, token: str) -> bool:
        r = await self._get_redis()
        return await r.get(f"blacklist:{token}") is not None
