from sport_network_api.ioc.providers.interactors.user import UserInteractorProvider
from sport_network_api.ioc.providers.interactors.account_settings import AccountSettingsInteractorProvider
from sport_network_api.ioc.providers.interactors.profile import ProfileInteractorProvider
from sport_network_api.ioc.providers.interactors.event import EventInteractorProvider


class InteractorProvider(
    UserInteractorProvider,
    AccountSettingsInteractorProvider,
    ProfileInteractorProvider,
    EventInteractorProvider,
):
    pass

__all__ = ["InteractorProvider"]
