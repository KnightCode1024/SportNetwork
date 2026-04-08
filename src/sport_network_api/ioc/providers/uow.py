from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from sport_network_api.application.interfaces.uow import UnitOfWorkInterface
from sport_network_api.infrastructure.unit_of_work import UnitOfWork


class UnitOfWorkProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_uow(self, session: AsyncSession) -> UnitOfWorkInterface:
        return UnitOfWork(session)
