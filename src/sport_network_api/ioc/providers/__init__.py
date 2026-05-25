from .auth import AuthProvider
from .config import ConfigProvider
from .database import DatabaseProvider
from .gateways import GatewayProvider
from .interactors import InteractorProvider
from .services import ServiceProvider
from .uow import UnitOfWorkProvider
from .cache import CacheProvider
from .clients import ClientsProvider

from dishka.integrations.fastapi import FastapiProvider

providers = [
    AuthProvider(),
    ConfigProvider(),
    DatabaseProvider(),
    UnitOfWorkProvider(),
    GatewayProvider(),
    InteractorProvider(),
    ServiceProvider(),
    FastapiProvider(),
    CacheProvider(),
    ClientsProvider(),
]

__all__ = ["providers"]
