from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, File, HTTPException, UploadFile, status

from sport_network_api.application.interactors.profile.interactors import (
    UploadAvatarInteractor,
)
from sport_network_api.controllers.schemas.profile import (
    UploadAvatarResponse,
)
from sport_network_api.controllers.schemas.user import UserResponse

router = APIRouter(
    prefix="/profile",
    tags=["Profile"],
    route_class=DishkaRoute,
)


# @router.get("", response_model=ProfileResponse)
# async def get_profile() -> ProfileResponse:
#     raise HTTPException(
#         status_code=status.HTTP_501_NOT_IMPLEMENTED,
#         detail="Get profile endpoint not implemented"
#     )


# @router.patch("", response_model=ProfileResponse)
# async def update_profile(
#     request: UpdateProfileRequest,
# ) -> ProfileResponse:
#     raise HTTPException(
#         status_code=status.HTTP_501_NOT_IMPLEMENTED,
#         detail="Update profile endpoint not implemented"
#     )


@router.post("/avatar", response_model=UploadAvatarResponse)
async def upload_avatar(
    current_user: FromDishka[UserResponse],
    interactor: FromDishka[UploadAvatarInteractor],
    file: UploadFile = File(),
) -> UploadAvatarResponse:
    try:
        avatar_url = await interactor(
            user_id=current_user.id,
            file_bytes=await file.read(),
            filename=file.filename or "avatar.jpg",
            content_type=file.content_type or "application/octet-stream",
        )
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err),
        ) from err

    return UploadAvatarResponse(avatar_url=avatar_url)


# @router.delete("/avatar", status_code=status.HTTP_200_OK)
# async def delete_avatar() -> dict:
#     raise HTTPException(
#         status_code=status.HTTP_501_NOT_IMPLEMENTED,
#         detail="Delete avatar endpoint not implemented"
#     )
