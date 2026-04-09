from fastapi import APIRouter, HTTPException, status
from dishka.integrations.fastapi import DishkaRoute, FromDishka

from sport_network_api.controllers.schemas.settings import (
    SettingsResponse,
    UpdateSettingsRequest,
    TwoFactorEnableResponse,
    TwoFactorDisableRequest,
)
from sport_network_api.controllers.schemas.user import UserResponse
from sport_network_api.application.interactors.settings.interactors import GetSettingsInteractor


router = APIRouter(
    prefix="/settings", 
    tags=["Settings"], 
    route_class=DishkaRoute,
)


@router.get("/", response_model=SettingsResponse)
async def get_settings(
    current_user: FromDishka[UserResponse],
    settings_interactor: FromDishka[GetSettingsInteractor],
) -> SettingsResponse:
    settings = await settings_interactor(current_user.id)
    return SettingsResponse(
        id=settings.id,
        user_id=settings.user_id,
        auth_2fa=settings.auth_2fa,
        notification_provider=settings.notification_provider.value if hasattr(settings.notification_provider, "value") else settings.notification_provider,
    )


# @router.patch("", response_model=SettingsResponse)
# async def update_settings(
#     request: UpdateSettingsRequest,
# ) -> SettingsResponse:
#     raise HTTPException(
#         status_code=status.HTTP_501_NOT_IMPLEMENTED,
#         detail="Update settings endpoint not implemented"
#     )
