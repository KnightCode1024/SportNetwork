from .auth import AuthProvider
from .config import ConfigProvider
from .database import DatabaseProvider
from .gateways import GatewayProvider
from .interactors import InteractorProvider
from .services import ServiceProvider
from dishka.integrations.fastapi import FastapiProvider

providers = [
    AuthProvider(),
    ConfigProvider(),
    DatabaseProvider(),
    GatewayProvider(),
    InteractorProvider(),
    ServiceProvider(),  
    FastapiProvider()
]


__all__ = ["providers"]
