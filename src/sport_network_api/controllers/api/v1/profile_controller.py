from fastapi import APIRouter, HTTPException, status, UploadFile, File

from sport_network_api.controllers.schemas.profile import (
    ProfileResponse,
    UpdateProfileRequest,
    UploadAvatarResponse,
)

router = APIRouter(prefix="/profile", tags=["Profile"])


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


# @router.post("/avatar", response_model=UploadAvatarResponse)
# async def upload_avatar(
#     file: UploadFile = File(),
# ) -> UploadAvatarResponse:
#     raise HTTPException(
#         status_code=status.HTTP_501_NOT_IMPLEMENTED,
#         detail="Upload avatar endpoint not implemented"
#     )


# @router.delete("/avatar", status_code=status.HTTP_200_OK)
# async def delete_avatar() -> dict:
#     raise HTTPException(
#         status_code=status.HTTP_501_NOT_IMPLEMENTED,
#         detail="Delete avatar endpoint not implemented"
#     )
