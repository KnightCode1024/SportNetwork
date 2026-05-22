from dishka import Provider, Scope, provide

from sport_network_api.application.interactors.profile.interactors import (
    UploadAvatarInteractor,
)
from sport_network_api.application.interfaces.gateways.profile_gateway import (
    ProfileGatewayInterface,
)
from sport_network_api.application.interfaces.services.s3_service import (
    S3ServiceInterface,
)
from sport_network_api.application.interfaces.uow.uow import UnitOfWorkInterface


class ProfileInteractorProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_upload_avatar_interactor(
        self,
        uow: UnitOfWorkInterface,
        profile_gateway: ProfileGatewayInterface,
        s3_service: S3ServiceInterface,
    ) -> UploadAvatarInteractor:
        return UploadAvatarInteractor(
            uow=uow,
            profile_gateway=profile_gateway,
            s3_service=s3_service,
        )
