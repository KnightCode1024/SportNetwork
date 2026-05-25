from dishka import Provider, Scope, provide

from sport_network_api.application.interactors.event.interactors import (
    ListEventsInteractor,
    GetEventInteractor,
    RegisterEventInteractor,
)
from sport_network_api.application.interfaces.gateways.event_gateway import (
    EventGatewayInterface,
)
from sport_network_api.application.interfaces.uow.uow import UnitOfWorkInterface


class EventInteractorProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_list_events_interactor(
        self,
        event_gateway: EventGatewayInterface,
    ) -> ListEventsInteractor:
        return ListEventsInteractor(event_gateway=event_gateway)

    @provide
    def get_event_detail_interactor(
        self,
        event_gateway: EventGatewayInterface,
    ) -> GetEventInteractor:
        return GetEventInteractor(event_gateway=event_gateway)

    @provide
    def get_register_event_interactor(
        self,
        uow: UnitOfWorkInterface,
        event_gateway: EventGatewayInterface,
    ) -> RegisterEventInteractor:
        return RegisterEventInteractor(
            uow=uow,
            event_gateway=event_gateway,
        )
