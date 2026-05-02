from dishka import Provider, Scope, provide

from sport_network_api.application.interactors.settings.interactors import (
    GetSettingsInteractor,
    UpdateSettingsInteractor,
)

from sport_network_api.application.interfaces.gateways.settings_gateway import SettingsGatewayInterface

from sport_network_api.application.interfaces.uow.uow import UnitOfWorkInterface


class AccountSettingsInteractorProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_settings_interactor(
            self,
            settings_gateway: SettingsGatewayInterface,
    ) -> GetSettingsInteractor:
        return GetSettingsInteractor(
            settings_gateway=settings_gateway,
        )

    @provide
    def get_update_settings_interactor(
            self,
            uow: UnitOfWorkInterface,
            settings_gateway: SettingsGatewayInterface,
    ) -> UpdateSettingsInteractor:
        return UpdateSettingsInteractor(
            uow=uow,
            settings_gateway=settings_gateway,
        )
