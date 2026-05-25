import time
import secrets


class StateStorage:
    def __init__(self, ttl_seconds: int = 300):
        self._store: dict[str, float] = {}
        self._ttl = ttl_seconds

    async def generate_and_store(self) -> str:
        state = secrets.token_urlsafe(16)
        self._store[state] = time.time()
        return state

    async def consume(self, state: str) -> bool:
        if state not in self._store:
            return False
        if time.time() - self._store[state] > self._ttl:
            del self._store[state]
            return False
        del self._store[state]
        return True
