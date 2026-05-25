from dishka import Provider, Scope, provide

from sport_network_api.application.interfaces.cache.oauth_storage import StateStorageInterface
from sport_network_api.infrastructure.cache.state_storage import StateStorage

class CacheProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_state_storage(self) -> StateStorageInterface:
        return StateStorage()
