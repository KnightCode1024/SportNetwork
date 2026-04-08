from typing import Protocol, AsyncContextManager
from sqlalchemy.ext.asyncio import AsyncSession


class UnitOfWorkInterface(Protocol):
    async def __aenter__(self):
        pass
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        pass
