from dishka import Provider, Scope, provide

from sport_network_api.application.interactors.profile.interactors import (
    UploadAvatarInteractor,
)
from sport_network_api.application.interfaces.gateways.profile_gateway import (
    ProfileGatewayInterface,
)
from sport_network_api.application.interfaces.gateways.s3_gateway import (
    S3GatewayInterface,
)
from sport_network_api.application.interfaces.uow.uow import UnitOfWorkInterface


class ProfileInteractorProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_upload_avatar_interactor(
        self,
        uow: UnitOfWorkInterface,
        profile_gateway: ProfileGatewayInterface,
        s3_gateway: S3GatewayInterface,
    ) -> UploadAvatarInteractor:
        return UploadAvatarInteractor(
            uow=uow,
            profile_gateway=profile_gateway,
            s3_gateway=s3_gateway,
        )
