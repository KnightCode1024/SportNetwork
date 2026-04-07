from fastapi import APIRouter
from dishka.integrations.fastapi import DishkaRoute

from .users_controller import router as users_router
from .profile_controller import router as profile_router 
from .settings_controller import router as settings_router 

v1_controller = APIRouter(
    prefix="/api/v1",
    route_class=DishkaRoute,
)

routers = [
    users_router,
    profile_router,
    settings_router,
]

for router in routers:
    v1_controller.include_router(router)


__all__ = ["v1_controller"]
