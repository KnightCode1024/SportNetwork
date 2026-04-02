from fastapi import APIRouter, HTTPException, status
from dishka.integrations.fastapi import DishkaRoute

from sport_network_api.controllers.schemas.settings import (
    SettingsResponse,
    UpdateSettingsRequest,
    TwoFactorEnableResponse,
    TwoFactorDisableRequest,
)


router = APIRouter(
    prefix="/settings", 
    tags=["Settings"], 
    route_class=DishkaRoute,
)


@router.get("", response_model=SettingsResponse)
async def get_settings(
) -> SettingsResponse:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Get settings endpoint not implemented"
    )


@router.patch("", response_model=SettingsResponse)
async def update_settings(
    request: UpdateSettingsRequest,
) -> SettingsResponse:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Update settings endpoint not implemented"
    )


@router.post("/2fa/enable", response_model=TwoFactorEnableResponse)
async def enable_2fa(
) -> TwoFactorEnableResponse:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Enable 2FA endpoint not implemented"
    )


@router.post("/2fa/disable", status_code=status.HTTP_200_OK)
async def disable_2fa(
    request: TwoFactorDisableRequest,
) -> dict:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Disable 2FA endpoint not implemented"
    )
