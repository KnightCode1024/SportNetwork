from sport_network_api.application.interfaces.gateways.profile_gateway import (
    ProfileGatewayInterface,
)
from sport_network_api.application.interfaces.gateways.s3_gateway import (
    S3GatewayInterface,
)
from sport_network_api.application.interfaces.uow.uow import UnitOfWorkInterface


class UploadAvatarInteractor:
    def __init__(
        self,
        uow: UnitOfWorkInterface,
        profile_gateway: ProfileGatewayInterface,
        s3_gateway: S3GatewayInterface,
    ):
        self.uow = uow
        self.profile_gateway = profile_gateway
        self.s3_gateway = s3_gateway

    async def __call__(
        self,
        user_id: int,
        file_bytes: bytes,
        filename: str,
        content_type: str,
    ) -> str:
        profile = await self.profile_gateway.get_by_user_id(user_id)
        if profile is None:
            raise ValueError("Profile not found")

        previous_avatar_url = profile.avatar_url
        avatar_url = await self.s3_gateway.upload_avatar(
            user_id=user_id,
            file_bytes=file_bytes,
            filename=filename,
            content_type=content_type,
        )

        try:
            async with self.uow:
                profile.set_avatar(avatar_url)
                await self.profile_gateway.update(profile)
        except Exception:
            avatar_key = self.s3_gateway.get_key_from_url(avatar_url)
            if avatar_key is not None:
                await self.s3_gateway.delete_file(avatar_key)
            raise

        if previous_avatar_url:
            previous_avatar_key = self.s3_gateway.get_key_from_url(previous_avatar_url)
            if previous_avatar_key is not None:
                await self.s3_gateway.delete_file(previous_avatar_key)

        return avatar_url
