from dishka import Provider, Scope, provide

from sport_network_api.ioc.providers.interactors.user import UserInteractorProvider
from sport_network_api.ioc.providers.interactors.account_settings import AccountSettingsInteractorProvider


class InteractorProvider(
    UserInteractorProvider,
    AccountSettingsInteractorProvider,
):
    pass

__all__ = ["InteractorProvider"]
