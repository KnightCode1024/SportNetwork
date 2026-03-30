from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from .users_controller import controller as user_controller

v1_controller = APIRouter(prefix="/v1", route_class=DishkaRoute)

controllers = [
    user_controller,
]

for controller in controllers:
    v1_controller.include_router(controller)


__all__ = [
    "v1_controller",
]

