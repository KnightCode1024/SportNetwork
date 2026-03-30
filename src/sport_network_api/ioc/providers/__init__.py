from .auth import AuthProvider
from .config import ConfigProvider
from .database import DatabaseProvider
from .gateways import GatewayProvider
from .interactors import InteractorProvider
from dishka.integrations.fastapi import FastapiProvider

providers = [
    AuthProvider(),
    ConfigProvider(),
    DatabaseProvider(),
    GatewayProvider(),
    InteractorProvider(),
    FastapiProvider()
]


__all__ = ["providers"]