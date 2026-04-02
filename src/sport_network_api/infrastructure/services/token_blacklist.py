class TokenBlacklistService:
    def __init__():
        pass

    async def get_redis(self):
        pass
    
    async def add_to_blacklist(self, token: str, ttl: int) -> None:
        pass
    
    async def is_blacklisted(self, token: str) -> bool:
        pass
    
    async def remove_from_blacklist(self, token: str) -> None:
        pass
    
    async def cleanup_expired(self) -> int:
        pass
    
    async def get_blacklist_count(self) -> int:
        pass
