from dishka import Provider, Scope, provide

from sport_network_api.application.interfaces.clients.google_oauth_client import GoogleOAuthClientInterface
from sport_network_api.infrastructure.oauth.google_client import GoogleOAuthClient
from sport_network_api.config.oauth.google import GoogleOAuthConfig

class ClientsProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_google_oauth_client(self, config: GoogleOAuthConfig) -> GoogleOAuthClientInterface:
        return GoogleOAuthClient(config)
